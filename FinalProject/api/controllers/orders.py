from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import menu_item as item_model
from ..models import promotions as promotions_model
from ..models import order_details as details_model
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError

from ..models.order_details import OrderDetail


def update_order_details(db, order, request):
    for item in request.items:
        candidate = db.query(item_model.MenuItem).filter(
            item_model.MenuItem.id == item.item.id).first()

        if candidate:
            mismatches = []
            if candidate.item_name != item.item.item_name:
                mismatches.append(f"item: expected '{candidate.item_name}', got '{item.item.item_name}'")
            if candidate.price != item.item.price:
                mismatches.append(f"price: expected '{candidate.price}', got '{item.item.price}'")
            if candidate.calories != item.item.calories:
                mismatches.append(f"calories: expected '{candidate.calories}', got '{item.item.calories}'")

            if mismatches:
                raise HTTPException(
                    status_code=400,
                    detail=f"Resource ID {item.item.id} mismatch: " + "; ".join(mismatches)
                )

        if not candidate:
            candidate = item_model.MenuItem(
                item_name=item.item.item_name,
                price=item.item.price,
                calories=item.item.calories,
                category=item.item.category
            )
            db.add(candidate)

        order.order_details.append(OrderDetail(
            menu_item=candidate,
            amount=item.amount
            )
        )



def create(db: Session, request):
    if request.promotion_code:
        promotion = db.query(promotions_model.Promotion).filter(
            promotions_model.Promotion.promotion_code == request.promotion_code).first()

    new_order = model.Order(
        date=datetime.now(),
        customer_name=request.customer_name,
        description=request.description,
        total_price=request.total_price,
        type=request.type,
        status=request.status# ,
        # promotion_id=promotion.id
    )

    update_order_details(db, new_order, request)
    
    try:
        db.add(new_order)
        db.flush()
        print(promotion.expiration_date > datetime.now())
        if promotion and (datetime.now() - promotion.expiration_date).total_seconds() < 0:
            new_order.calculate_total_price(promotion.discount)
        else:
            new_order.calculate_total_price()
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_order


def create_cart(db, request):
    if db.query(model.Order).filter(
            model.Order.customer_name == request.customer_name,
            model.Order.order_placed.is_(None)).first() is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cart already exists")
    new_order = create(db, request)
    return new_order

def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def update(db: Session, order_id, request):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.dict(exclude_unset=True)

        if "order_Details" in update_data:
            update_data.pop("resources")

        for key, value in update_data.items():
            setattr(order, key, value)

        db.query(details_model.OrderDetail).filter(details_model.OrderDetail.order_id == order_id).delete()

        update_order_details(db, order, request)
        db.flush()
        order.calculate_total_price()
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def review(db: Session, order_id, request):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        order.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def delete(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        db.delete(order)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def place_order(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        elif not order.first().order_placed:
            order.update({"status": "Your order has been placed"}, synchronize_session=False)
            order.update({"order_placed": datetime.now()}, synchronize_session=False)
            db.commit()
        else:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order has already been placed")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()

def cancel_order(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        elif order.first().order_placed and not order.first().order_canceled and not order.first().order_ready:
            order.update({"status": "Your order has been canceled"}, synchronize_session=False)
            order.update({"order_canceled": datetime.now()}, synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order either hasn't been placed, or is already canceled")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def prep_order(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        elif order.first().order_placed and not order.first().order_canceled and not order.first().order_prepping:
            order.update({"status": "Your order is bein prepped"}, synchronize_session=False)
            order.update({"order_prepping": datetime.now()}, synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order either hasn't been placed, is already being prepped, or is already canceled")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def ready_order(db: Session, order_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        elif (order.first().order_placed and order.first().order_prepping and not order.first().order_ready) and not order.first().order_canceled:
            order.update({"status": "Your order is ready"}, synchronize_session=False)
            order.update({"order_ready": datetime.now()}, synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order either hasn't been placed, isn't being prepped yet, is already ready, or is already canceled")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def cart_add_item(db: Session, order_id, request):
    try:
        order = db.query(model.Order).filter(
            model.Order.id == order_id).first()
        item = db.query(item_model.MenuItem).filter(
            item_model.MenuItem.id == request.item.id).first()

        if not order or not item:
            raise HTTPException(status_code=404, detail="Order or item not found")

        if order.order_placed:
            raise HTTPException(status_code=403, detail="Order is not a cart")

        candidate = db.query(details_model.OrderDetail).filter(
            details_model.OrderDetail.order_id == order_id,
            details_model.OrderDetail.item_id == request.item.id).first()

        if candidate:
            candidate.amount += request.amount
        else:
            db.add(details_model.OrderDetail(
                order_id=order_id,
                item_id=item.id,
                amount=request.amount
            ))
        order.calculate_total_price()
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def cart_remove_item(db: Session, order_id, request):
    try:
        order = db.query(model.Order).filter(
            model.Order.id == order_id).first()
        item = db.query(item_model.MenuItem).filter(
            item_model.MenuItem.id == request.item.id).first()

        if not order or not item:
            raise HTTPException(status_code=404, detail="Order or item not found")

        if order.order_placed:
            raise HTTPException(status_code=403, detail="Order is not a cart")

        candidate = db.query(details_model.OrderDetail).filter(
            details_model.OrderDetail.order_id == order_id,
            details_model.OrderDetail.item_id == request.item.id).first()

        if candidate:
            candidate.amount -= request.amount

            if candidate.amount <= 0:
                db.delete(candidate)
        else:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        order.calculate_total_price()
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def get_status(db, order_id):
    try:
        order = db.query(model.Order).filter(
            model.Order.id == order_id).first()

        order_status = {"status": str, "time": datetime}

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if not order.order_placed:
            raise HTTPException(status_code=403, detail="Order is still in cart")

        if order.order_canceled:
            raise HTTPException(status_code=403, detail="Order is cancelled")

        if order.order_ready:
            return {"status": "ready", "time": (datetime.now() - order.order_ready).total_seconds()}
        elif order.order_prepping:
            return {"status": "prepping", "time": (datetime.now() - order.order_prepping).total_seconds()}
        else:
            return {"status": "placed", "time": (datetime.now() - order.order_placed).total_seconds()}
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
'''
def rate_orders(db: Session, order_id):
    # Assign orders a blue like 1-5.
    # Create an orders list.
    orders = db.query(model.Order)

    # Access review_rating.
    ratings = db.query(model.review_rating)

    # return back a proper rating.
    for rating in ratings:
        if rating == 1:
            return 1

        elif rating == 2:
            return 2
 
        elif rating == 3:
            return 3

        elif rating == 4:
            return 4
        
        elif rating == 5:
            return 5
    # Function 5: Allow the user to review order
    def review_orders():
        # Allow user to create a description.
        description = input("Please enter a review: ")
        return description'''

from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import menu_item as item_model
from ..models import order_details as details_model
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
    new_order = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        total_price=request.total_price,
        type=request.type,
        status=request.status,
        promotion_code=request.promotion_code
    )

    update_order_details(db, new_order, request)

    try:
        db.add(new_order)
        db.flush()
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


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


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


def delete(db: Session, item_id):
    try:
        order = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        db.delete(order)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

 
def place_order(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        #item.order_placed = datetime.now()
        item.update({"order_placed": datetime.now()}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def cancel_order(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"order_canceled": datetime.now()}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def prep_order(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"order_prepping": datetime.now()}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def ready_order(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"order_ready": datetime.now()}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def cart_add_item(db: Session, order_id, request):
    try:
        order = db.query(model.Order).filter(
            model.Order.id == order_id).first()
        item = db.query(item_model.MenuItem).filter(
            item_model.MenuItem.id == request.item.id).first()

        if not order or not item:
            raise HTTPException(status_code=404, detail="Order or item not found")

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





def analyze_data():
    pass

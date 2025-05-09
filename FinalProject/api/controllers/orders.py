from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from . import order_details
from ..models import orders as model
from ..models import menu_item as item_model
from ..models import promotions as promotions_model
from ..models import order_details as details_model
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError




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


def check_resources(order):
    for detail in order.order_details:
        menu_item = detail.menu_item
        recipe = menu_item.recipe
        for recipe_resource in recipe.resources_link:
            required_amount = detail.amount * float(recipe_resource.amount)
            if recipe_resource.resource.amount < required_amount:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient resource: {recipe_resource.resource.item}"
                )


def update_resources(order):
    check_resources(order)

    # Deduct resources
    for detail in order.order_details:
        for recipe_resource in detail.menu_item.recipe.resources_link:
            used_amount = detail.amount * recipe_resource.amount
            recipe_resource.resource.amount -= used_amount


def create(db: Session, request):
    promotion = None
    if request.promotion_code:
        promotion = db.query(promotions_model.Promotion).filter(
            promotions_model.Promotion.promotion_code == request.promotion_code).first()

    new_order = model.Order(
        date=datetime.now(),
        customer_name=request.customer_name,
        description=request.description,
        total_price=request.total_price,
        type=request.type,
        status=request.status
        # promotion_id=promotion.id
    )

    update_order_details(db, new_order, request)

    check_resources(new_order)
    
    try:
        db.add(new_order)
        db.flush()
        if promotion:
            print(promotion.expiration_date > datetime.now())
            if promotion and (datetime.now() - promotion.expiration_date).total_seconds() < 0:
                new_order.calculate_total_price(promotion.discount)
            else:
                new_order.calculate_total_price()
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
        check_resources(order)
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
        order_query = (db.query(model.Order).filter(model.Order.id == order_id))
        order = order_query.first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        if order.order_placed:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order has already been placed")

        update_resources(order)

        order_query.update({"status": "Your order has been placed"}, synchronize_session=False)
        order_query.update({"order_placed": datetime.now()}, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order

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

        check_resources(order)
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


def get_orders_between_dates(db: Session, start_date: datetime, end_date: datetime):
    orders = db.query(Order).filter(Order.order_placed != None).filter(
        Order.order_placed >= start_date,
        Order.order_placed <= end_date
    ).all()
    return orders


# Sums the price of all orders between given dates
def calculate_sum_profit_between_days(db: Session, start_date: datetime, end_date: datetime):
    sum_profit = db.query(func.sum(model.Order.total_price)).filter(
        model.Order.order_ready >= start_date,
        model.Order.order_ready <= end_date
    ).scalar()

    return sum_profit
'''
# Function 2: Create a function that lists the average amount of time between order statuses.
def average_time_between_order_statuses(db: Session, order_id):
    # Retrieve order information by query().
    orders = db.query(model.Order).filter(model.Order.order_ready)

    # Once list of orders retrieved get the time between orders.
    order_placed_times = orders.filter(
        model.Order.order_placed == order_id).all()  # Represents the times an order is placed.

    # Create some needed values.
    sum_of_time = 0.0  # Represents the amount of time added up.

    count = 0  # Represents the amount of numbers in list.

    # Iterate through the list through list.
    for order_placed_time in order_placed_times:
        # Add up all the times.
        sum_of_time += order_placed_time
        # Keep track of the amount of numbers to divide by.
        count += 1

    # Calculate average.
    average_time = sum_of_time / count

    return average_time


# Function 3: Create a function that list items by amount of orders.
def list_order_amount_by_item(db: Session, item_id):
    # Retrieve a list of all orders.
    orders = db.query(model.Order)

    # Retrieve order details.
    order_details = db.query(details_model.OrderDetail)

    # Make a list of all items from orders.
    list_of_items = db.query(item_model.MenuItem)

    count = 0

    for order in orders:
        for detail in order_details:
            if (detail.item_id == item_id):
                count += 1

    return count
'''

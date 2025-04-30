from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError



def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


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


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Add functions for data analyzing in this file:

# Function 1: Create a function that calculates the sum profit between days.
def calculate_sum_profit_between_days(db: Session, order_id, start_date, end_date):
    # Retrieve order information by query().
    orders = db.query(model.Order).filter(model.Order.order_ready >= start_date).filter(model.Order.order_ready <= end_date).all()

    # Create a sum_profit.
    sum_profit = 0

    # Iterate over a loop and add results up to sum.
    for order in orders:
        if order_id == order.id:
            sum_profit += order.profit

    # Once sum is calculated return the sum.
    return sum_profit

# Function 2: Create a function that lists the average amount of time between order statuses.
def average_time_between_order_statuses(db: Session, order_id):
    # Retrieve order information by query().
    orders = db.query(model.Order).filter(model.Order.order_ready)

    # Once list of orders retrieved get the time between orders.
    order_placed_times = orders.filter(model.Order.order_placed == order_id).all() # Represents the times an order is placed.

    # Create some needed values.
    sum_of_time = 0.0 # Represents the amount of time added up.
    count = 0 # Represents the amount of numbers in list.

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
def list_items_by_amount_of_order(db: Session, order_id):
    # Sorted list of items.
    sorted_list = []

    # Retrieve a list of all orders.
    orders = db.query(model.Order)

    # Make a list of all items from orders.
    list_of_items = orders.items

    # Once you have the items sort them greatest to least.
    greatest_item = list_of_items[0]

    for current_item in list_of_items:
        if current_item.amount > greatest_item.amount:
            greatest_item = current_item
            sorted_list.append(greatest_item)

    return sorted_list


# Create functions that will allow you to give a rating of 1-5 or 1-10 to the orders table.
# also create a function that will allow you leave review for orders. Specifically a string.

# Function 4: Allow user to rate their orders.
def rate_orders():
    # Assign orders a value like 1-5.

    pass

# Function 5: Allow the user to review order
def review_orders():
    # Allow user to create a description.
    pass






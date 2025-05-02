from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from sqlalchemy.testing.pickleable import Order
from ..controllers import orders as controller
from ..main import app
import pytest


# Create a test client for the app
client = TestClient(app)

# Here is the code skeleton.
def test_calculate_sum_profit_between_days(start_date,end_date):
    # Create an object.
    my_order_obj = Order()
    # Test function by call.
    #my_order_obj.calculate_sum_profit_between_days(db: Session, order_id, start_date, end_date)


def test_average_time_between_order_statuses(order_id=None):
    # Create an object.
    my_order_obj = Order()
    # Test function by call.
    #my_order_obj.average_time_between_order_statuses(db: Session, order_id)


def test_list_items_by_amount_of_order():
    # Create an object.
    my_order_obj = Order()
    # Test function by call.
    #my_order_obj.list_items_by_amount_of_order(db: Session, order_id)


def test_rate_orders():
    # Create an object.
    my_order_obj = Order()
    # Test function by call.
    #my_order_obj.rate_orders(db: Session, order_id)


def test_review_orders():
    # Create an object.
    my_order_obj = Order()
    # Test function by call.
    #my_order_obj.review_orders():
from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
 

# Create a test client for the app
client = TestClient(app)


# Here is the code skeleton.
def test_calculate_sum_profit_between_days():
    pass


def test_average_time_between_order_statuses():
    pass


def test_list_items_by_amount_of_order():
    pass


def test_rate_orders():
    pass


def test_review_orders():
    pass

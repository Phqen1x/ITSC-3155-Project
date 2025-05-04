from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, status, Response, Query
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from ..schemas.orders import OrderStatusUpdate

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.post("/cart/create", response_model=schema.Order)
def create_cart(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create_cart(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/between-dates", response_model=List[schema.Order])
def get_orders_by_date_range(
    start_date: datetime = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: datetime = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    return controller.get_orders_between_dates(db, start_date, end_date)


@router.get("/{order_id}", response_model=schema.Order)
def read_one(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id=order_id)


@router.get("/status/{order_id}", response_model=schema.OrderStatus)
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    return controller.get_status(db, order_id=order_id)


@router.put("/customer/{order_id}", response_model=schema.Order)
def update_customer(order_id: int, request: schema.OrderUpdateCustomer, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.put("/review/{order_id}", response_model=schema.Order)
def review_order(order_id: int, request: schema.OrderReview, db: Session = Depends(get_db)):
    return controller.review(db=db, request=request, order_id=order_id)


@router.put("/restaurant/{order_id}", response_model=schema.Order)
def update_restaurant(order_id: int, request: schema.OrderUpdateRestaurant, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.put("/cart/add_item/{order_id}/", response_model=schema.Order)
def cart_add_item(order_id:int,request: schema.ItemsInOrder, db: Session = Depends(get_db)):
    return controller.cart_add_item(db=db, request=request,order_id=order_id)

@router.put("/cart/remove_item/{order_id}/", response_model=schema.Order)
def cart_remove_item(order_id:int,request: schema.ItemsInOrder, db: Session = Depends(get_db)):
    return controller.cart_remove_item(db=db, request=request,order_id=order_id)


@router.put("/{order_id}/place_order", response_model=schema.Order)
def place_order(order_id: int, db: Session = Depends(get_db)):
    return controller.place_order(db=db, order_id=order_id)


@router.put("/{order_id}/cancel_order", response_model=schema.Order)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    return controller.cancel_order(db=db, order_id=order_id)


@router.put("/{order_id}/prep_order", response_model=schema.Order)
def prep_order(order_id: int, db: Session = Depends(get_db)):
    return controller.prep_order(db=db, order_id=order_id)


@router.put("/{order_id}/ready_order", response_model=schema.Order)
def ready_order(order_id: int, db: Session = Depends(get_db)):
    return controller.ready_order(db=db, order_id=order_id)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)

# Endpoints of unique features.
'''
@router.get("/sum_profits")
def sum_profit_by_date_range():
    # start_date: datetime = Query(..., description="Start date in format YYYY-MM-DD"),
    # end_date: datetime = Query(..., description="End date in format YYYY-MM-DD"),
    # db: Session = Depends(get_db)
    # ):
    print("sum_profit_by_date_range")
    # return controller.calculate_sum_profit_between_days(db, start_date, end_date)
    return "foo"
'''

@router.get("/{item_id}", response_model=schema.Order)
def list_order_amount_by_item(item_id: int, db: Session = Depends(get_db)):
    return controller.list_order_amount_by_item(db, item_id=item_id)

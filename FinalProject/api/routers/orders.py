from datetime import datetime
from fastapi import Query
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

# Endpoints of unique features.

@router.get("/sum-profits", response_model=List[schema.Order])
def sum_profit_by_date_range(
    start_date: datetime = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: datetime = Query(..., description="End date in format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    return controller.calculate_sum_profit_between_days(db, start_date, end_date)



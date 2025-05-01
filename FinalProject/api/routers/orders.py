from fastapi import APIRouter, Depends, FastAPI, status, Response
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


@router.post("/create_cart", response_model=schema.Order)
def create_cart(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create_cart(db=db, request=request)



@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update_customer(item_id: int, request: schema.OrderUpdateCustomer, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update_restaurant(item_id: int, request: schema.OrderUpdateRestaurant, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


@router.put("/{item_id}/place_order", response_model=schema.Order)
def place_order(item_id: int, db: Session = Depends(get_db)):
    return controller.place_order(db=db, item_id=item_id)


@router.put("/{item_id}/cancel_order", response_model=schema.Order)
def cancel_order(item_id: int, db: Session = Depends(get_db)):
    return controller.cancel_order(db=db, item_id=item_id)


@router.put("/{item_id}/prep_order", response_model=schema.Order)
def prep_order(item_id: int, db: Session = Depends(get_db)):
    return controller.prep_order(db=db, item_id=item_id)


@router.put("/{item_id}/ready_order", response_model=schema.Order)
def ready_order(item_id: int, db: Session = Depends(get_db)):
    return controller.ready_order(db=db, item_id=item_id)
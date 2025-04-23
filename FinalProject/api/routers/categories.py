from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import categories as controller
from ..schemas import categories as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Categories'],
    prefix="/categories",
)


@router.post("/", response_model=schema.Category)
def create(request: schema.CategoryCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Category])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{category_id}", response_model=schema.Category)
def read_one(category_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, category_id=category_id)


@router.put("/{category_id}", response_model=schema.Category)
def update(category_id: int, request: schema.CategoryUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, category_id=category_id)


@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, category_id=category_id)

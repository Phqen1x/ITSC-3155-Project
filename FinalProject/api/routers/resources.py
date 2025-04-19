from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Resources'],
    prefix="/resources"
)


@router.post("/", response_model=schema.Resource)
def create(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Resource])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{ingredient_id}", response_model=schema.Resource)
def read_one(ingredient_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, ingredient_id=ingredient_id)


@router.put("/{ingredient_id}", response_model=schema.Resource)
def update(ingredient_id: int, request: schema.ResourceUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, ingredient_id=ingredient_id)


@router.delete("/{ingredient_id}")
def delete(ingredient_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, ingredient_id=ingredient_id)

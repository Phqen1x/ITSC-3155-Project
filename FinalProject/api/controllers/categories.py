from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import categories as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_category = model.Category(
        type=request.type
    )

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_category


def read_all(db: Session):
    try:
        result = db.query(model.Category).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, category_id):
    try:
        ingredient = db.query(model.Category).filter(model.Category.id == category_id).first()
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient


def update(db: Session, category_id, request):
    try:
        ingredient = db.query(model.Category).filter(model.Category.id == category_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        ingredient.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient.first()


def delete(db: Session, category_id):
    try:
        ingredient = db.query(model.Category).filter(model.Category.id == category_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        ingredient.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

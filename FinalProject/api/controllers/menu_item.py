from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import MenuItem as model
from sqlalchemy.exc import SQLAlchemyError

# Newly created file by Tareq
def create(db: Session, request):
    new_item = model.MenuItem(
        item_name=request.item_name,
        price=request.price,
        calories=request.calories,
        category=request.category
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        # error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.MenuItem).all()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        ingredient = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient


def update(db: Session, item_id, request):
    try:
        ingredient = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
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


def delete(db: Session, item_id):
    try:
        ingredient = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        ingredient.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

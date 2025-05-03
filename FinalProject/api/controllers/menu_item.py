from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_item as model
from sqlalchemy.exc import SQLAlchemyError

from ..models.recipes import Recipe
from ..models.recipes_categories import RecipesCategories


# Newly created file by Tareq
def create(db: Session, request):
    recipe = db.query(Recipe).filter_by(id=request.recipe).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    new_item = model.MenuItem(
        item_name=request.item_name,
        recipe=recipe,
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.MenuItem).all()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        ingredient = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient


def update(db: Session, item_id, request):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        ingredient = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        ingredient.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def read_category(db, request):
    category_ids = [category.category.id for category in request.categories]
    try:
        if request.search_and:
           items = ((((db.query(model.MenuItem)
                    .join(model.MenuItem.recipe))
                    .join(Recipe.categories_link))
                    .filter(RecipesCategories.category_id.in_(category_ids))
                    .distinct().all()))
        else:
            category_count = len(category_ids)
            subquery = (
                db.query(Recipe.id.label("recipe_id"))
                .join(RecipesCategories)
                .filter(RecipesCategories.category_id.in_(category_ids))
                .group_by(Recipe.id)
                .having(func.count(RecipesCategories.category_id.distinct()) == category_count)
                .subquery()
            )
            items = (((db.query(model.MenuItem)
                     .join(model.MenuItem.recipe))
                     .join(subquery, Recipe.id == subquery.c.recipe_id))
                     .all())
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return items
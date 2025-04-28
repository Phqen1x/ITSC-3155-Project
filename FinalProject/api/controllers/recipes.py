from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response, Depends
from ..models import recipes as model
from ..models import resources as resource_model
from sqlalchemy.exc import SQLAlchemyError

from ..models.recipes_resources import RecipesResource
from ..models.resources import Resource


def update_recipes_resources(db, recipe, request):
    for ingredient in request.resources:
        candidate = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == ingredient.resource.id).first()

        if candidate:
            mismatches = []
            if candidate.item != ingredient.resource.item:
                mismatches.append(f"item: expected '{candidate.item}', got '{ingredient.resource.item}'")
            if candidate.unit != ingredient.resource.unit:
                mismatches.append(f"unit: expected '{candidate.unit}', got '{ingredient.resource.unit}'")

            if mismatches:
                raise HTTPException(
                    status_code=400,
                    detail=f"Resource ID {ingredient.resource.id} mismatch: " + "; ".join(mismatches)
                )

        if not candidate:
            candidate = resource_model.Resource(
                item=ingredient.resource.item,
                amount=ingredient.resource.amount,
                unit=ingredient.resource.unit
            )
            db.add(candidate)

        recipe.resources_link.append(RecipesResource(
            resource=candidate,
            amount=ingredient.amount
        ))


def create(db: Session, request):
    new_recipe = model.Recipe(

    )

    update_recipes_resources(db, new_recipe, request)

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as e:
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_recipe


def read_all(db: Session):
    try:
        result = db.query(model.Recipe).options(
            joinedload(model.Recipe.resources_link).joinedload(model.RecipesResource.resource)
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, recipe_id):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe


def update(db: Session, recipe_id, request):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)

        if "resources" in update_data:
            update_data.pop("resources")

        for key, value in update_data.items():
            setattr(recipe, key, value)

        db.query(RecipesResource).filter(RecipesResource.recipe_id == recipe_id).delete()

        update_recipes_resources(db, recipe, request)
        db.commit()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe


def delete(db: Session, recipe_id):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        db.delete(recipe, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        # error = str(e.__dict__['orig'])
        error = str(getattr(e, 'orig', 'No original error found'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

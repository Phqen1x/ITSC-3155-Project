from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
from ..controllers import menu_item as controller
from ..schemas import menu_item as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['MenuItem'],
    prefix="/menu_item",
)

# Create a new menu item
@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

# Read all menu items
@router.get("/", response_model=list[schema.MenuItem])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

#Get menu by categories
@router.get("/categories", response_model=List[schema.MenuItem])
def read_category(category_ids: Annotated[List[int], Query()],
    search_and: bool = False,
    db: Session = Depends(get_db)
):
    return controller.read_category(db, category_ids=category_ids, search_and=search_and)

# Read a specific menu item
@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


# Update a specific menu item
@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

# Delete specific menu item
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

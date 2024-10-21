from typing import Annotated

from fastapi import APIRouter, Depends
from slugify import slugify
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    categories = db.scalars(select(Category).where(Category.is_active == True)).all()
    return categories


@router.post('/create')
async def create_category(db: Annotated[Session, Depends(get_db)], create_category: CreateCategory):
    db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parent_id,
                                       slug=slugify(create_category.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successfully created'
    }


@router.put('/update_category')
async def update_category():
    pass


@router.delete('/delete')
async def delete_category():
    pass

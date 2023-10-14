from fastapi import APIRouter
from fastapi import Depends, status
from api.models import schemas
from database.dependencies import get_db
from sqlalchemy.orm import Session
from api import crud

router = APIRouter(
    prefix="/store",
    tags=["store"],
)


@router.get(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Store]
)
def read_store_by_phone(phone, db: Session = Depends(get_db)):
    return crud.get_stores_by_phone(phone, db)

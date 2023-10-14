from fastapi import APIRouter
from fastapi import Depends, status
from api.models import schemas
from database.dependencies import get_db
from sqlalchemy.orm import Session
from api import crud


router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Order]
)
def read_order_by_phone(phone, db: Session = Depends(get_db)):
    return crud.get_orders_by_phone(phone, db)


@router.post(
    "/{phone}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Order)
def create_order_by_phone(
        phone,
        order: schemas.OrderCreate,
        db: Session = Depends(get_db)
):
    return crud.post_order_by_phone(phone, db=db, order=order)


@router.delete(
    "/{phone}",
    status_code=status.HTTP_200_OK,
)
def remove_order_by_phone(
        phone,
        order: schemas.OrderDelete,
        db: Session = Depends(get_db)
):
    return crud.delete_order_by_phone(phone, db=db, order=order)


@router.put(
    "/{phone}",
    status_code=status.HTTP_200_OK,
)
def update_order_by_phone(
        phone,
        order: schemas.OrderUpdate,
        db: Session = Depends(get_db)
):
    return crud.put_order_by_phone(phone, db=db, order=order)

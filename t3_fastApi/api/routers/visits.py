from fastapi import APIRouter
from fastapi import Depends, status
from api.models import schemas
from database.dependencies import get_db
from sqlalchemy.orm import Session
from api import crud

router = APIRouter(
    prefix="/visit",
    tags=["visit"],
)


@router.get(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Visit]
)
def read_visit_by_phone(phone, db: Session = Depends(get_db)):
    return crud.get_visits_by_phone(phone, db)


@router.post(
    "/{phone}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Visit
)
def create_visit_by_phone(
        phone,
        visit: schemas.VisitCreate,
        db: Session = Depends(get_db)
):
    return crud.post_visits_by_phone(phone, db=db, visit=visit)


@router.delete(
    "/{phone}",
    status_code=status.HTTP_200_OK,
)
def remove_order_by_phone(
        phone,
        visit: schemas.VisitDelete,
        db: Session = Depends(get_db)
):
    return crud.delete_visit_by_phone(phone, db=db, visit=visit)

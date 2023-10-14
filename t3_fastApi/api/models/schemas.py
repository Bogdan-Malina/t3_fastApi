from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import validator
from database.models.models import Statuses
import enum


class WorkerBase(BaseModel):
    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    class Config:
        orm_mode = True


class VisitBase(BaseModel):
    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    class Config:
        orm_mode = True


class WorkerCreate(WorkerBase):
    name: str
    phone_number: str


class Worker(WorkerBase):
    id: int
    name: str
    phone_number: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    name: str
    phone_number: str


class StoreCreate(StoreBase):
    name: str


class Store(StoreBase):
    id: int
    name: str


class OrderCreate(OrderBase):
    where_id: int
    executor_id: int
    close_date: datetime
    status: str

    @validator("status")
    @classmethod
    def check_key(cls, v) -> str:
        if v not in Statuses.get_status():
            raise HTTPException(
                status_code=400,
                detail="Status is not a valid"
            )
        return v


class Order(OrderBase):
    where: Store
    author: Customer
    executor: Worker
    create_date: datetime
    close_date: datetime
    status: enum.Enum

    @validator("status")
    @classmethod
    def chose_to_str(cls, v) -> str:
        return v.value


class OrderDelete(OrderBase):
    id: int


class OrderUpdate(OrderBase):
    id: int
    status: str

    @validator("status")
    @classmethod
    def check_key(cls, v) -> str:
        if v not in Statuses.get_status():
            raise HTTPException(
                status_code=400,
                detail="Status is not a valid"
            )
        return v


class VisitCreate(VisitBase):
    order_id: int


class Visit(VisitBase):
    id: int
    create_date: datetime
    executor: Worker
    order: Order
    author: Customer
    where: Store


class VisitDelete(VisitBase):
    id: int

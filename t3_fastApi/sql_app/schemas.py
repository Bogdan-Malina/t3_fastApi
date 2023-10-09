import typing
from datetime import datetime
from pydantic import BaseModel
from pydantic import validator


class WorkerBase(BaseModel):
    pass


class StoreBase(BaseModel):
    pass


class OrderBase(BaseModel):
    pass


class CustomerBase(BaseModel):
    pass


class WorkerCreate(WorkerBase):
    name: str
    phone_number: str
    # store_id: int


class Worker(WorkerBase):
    id: int
    name: str
    phone_number: str

    # stores: list["Store"]

    class Config:
        orm_mode = True


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    name: str
    phone_number: str

    class Config:
        orm_mode = True


class StoreCreate(StoreBase):
    name: str


class Store(StoreBase):
    id: int
    name: str

    # workers: list[Worker] = []
    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    where: Store
    author: Customer
    executor: Worker
    create_date: datetime
    close_date: datetime
    status: typing.Any

    @validator("status")
    @classmethod
    def double(cls, v) -> str:
        return v.code

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    # class ItemBase(BaseModel):
#     title: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
# class UserBase(BaseModel):
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#
#     class Config:
#         orm_mode = True

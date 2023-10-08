from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True



class WorkerBase(BaseModel):
    pass

class StoreBase(BaseModel):
    pass


class WorkerCreate(WorkerBase):
    name: str
    phone_number: str
    store_id: int


class Worker(WorkerBase):
    id: int
    name: str
    phone_number: str
    store_id: int
    
    class Config:
        orm_mode = True


class StoreCreate(StoreBase):
    name: str


class Store(StoreBase):
    id: int
    name: str
    workers: list[Worker] = []

    class Config:
        orm_mode = True
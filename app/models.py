from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import relationship

from .database import Base


class User(Base): # STORE
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base): # WORKER
    __tablename__ = "items"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True)
    description = sqlalchemy.Column(sqlalchemy.String, index=True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Worker(Base):  # OK
    __tablename__ = "worker"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String(255), index=True)

    store_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stores.id"))
    store = relationship("Store", back_populates="worker")
    executor = relationship("Order", back_populates="executor")
    executor_visit = relationship("Visit", back_populates="executor")
    # executor_store = relationship("Store", back_populates="executor")
    

class Customer(Base):  # OK
    __tablename__ = "customer"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    
    store_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stores.id"))
    store = relationship("Store", back_populates="customer")
    author = relationship("Order", back_populates="author")
    author_visit = relationship("Visit", back_populates="author")


class Store(Base):  # OK
    __tablename__ = "stores"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    worker_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("worker.id"))
    
    worker = relationship("Worker", back_populates="store")
    customer = relationship("Customer", back_populates="store")
    where = relationship("Order", back_populates="where")
    where_visit = relationship("Visit", back_populates="where")


class Order(Base):  # OK
    __tablename__ = "order"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    create_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.utcnow)
    close_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    status = sqlalchemy.Column(sqlalchemy.String['started', 'ended', 'in process', 'awaiting', 'canceled'])
    
    where_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stores.id"))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("customer.id"))
    executor_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("worker.id"))
    
    where = relationship("Store", back_populates="where")
    author = relationship("Customer", back_populates="author")
    executor = relationship("Worker", back_populates="executor")
    order = relationship("Visit", back_populates="order")


class Visit(Base):  # OK
    __tablename__ = "visit"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    create_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.utcnow)
    
    executor_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("worker.id"))
    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("order.id"))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("customer.id"))
    where_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stores.id"))
    
    executor = relationship("Worker", back_populates="executor_visit")
    order = relationship("Order", back_populates="order")
    author = relationship("Customer", back_populates="author_visit")
    where = relationship("Store", back_populates="where_visit")

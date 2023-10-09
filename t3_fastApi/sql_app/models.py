from datetime import datetime

import sqlalchemy
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List, Optional

from .database import Base


customer_store = sqlalchemy.Table(
    "customer_store",
    Base.metadata,
    sqlalchemy.Column(
        "customer_id",
        sqlalchemy.ForeignKey("customer_table.id"),
        primary_key=True,
        nullable=False
    ),
    sqlalchemy.Column(
        "store_id",
        sqlalchemy.ForeignKey("store_table.id"),
        primary_key=True,
        nullable=False
    ),
)

worker_store = sqlalchemy.Table(
    "worker_store",
    Base.metadata,
    sqlalchemy.Column(
        "worker_id",
        sqlalchemy.ForeignKey("worker_table.id"),
        primary_key=True,
        nullable=False
    ),
    sqlalchemy.Column(
        "store_id",
        sqlalchemy.ForeignKey("store_table.id"),
        primary_key=True,
        nullable=False
    ),
)


class Store(Base):
    __tablename__ = "store_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(255))

    # workers: Mapped[List["Worker"]] = relationship(back_populates="store")
    workers: Mapped[List["Worker"]] = relationship(
        secondary=worker_store, back_populates="stores"
    )
    # customers: Mapped[List["Customer"]] = relationship(back_populates="store")
    customers: Mapped[List["Customer"]] = relationship(
        secondary=customer_store, back_populates="stores"
    )

    def __str__(self):
        return self.name


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(255))
    phone_number: Mapped[str] = mapped_column(sqlalchemy.String(255))

    # store_id: Mapped[int] = mapped_column(
    #     sqlalchemy.ForeignKey("store_table.id"),
    #     nullable=False
    # )
    # stores: Mapped[list["Store"]] = relationship(back_populates="customers")
    stores: Mapped[List["Store"]] = relationship(
        secondary=customer_store, back_populates="customers"
    )

    def __str__(self):
        return self.name


class Worker(Base):
    __tablename__ = "worker_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(255))
    phone_number: Mapped[str] = mapped_column(sqlalchemy.String(255))

    # store_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("store_table.id"))
    # store: Mapped["Store"] = relationship(back_populates="workers")
    stores: Mapped[List["Store"]] = relationship(
        secondary=worker_store, back_populates="workers"
    )

    def __str__(self):
        return self.name


class Order(Base):
    __tablename__ = "order_table"
    STATUSES = [
        ("started", "Started"),
        ("ended", "Ended"),
        ("in_process", "In process"),
        ("awaiting", "Awaiting"),
        ("canceled", "Canceled")
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP,
        default=datetime.utcnow
    )
    close_date: Mapped[datetime] = mapped_column(sqlalchemy.TIMESTAMP)
    status: Mapped[str] = mapped_column(
        ChoiceType(STATUSES, impl=sqlalchemy.String())
    )

    where_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("store_table.id"))
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("customer_table.id"))
    executor_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("worker_table.id"))

    where: Mapped["Store"] = relationship()
    author: Mapped["Customer"] = relationship()
    executor: Mapped["Worker"] = relationship()

    def __str__(self):
        return f"{self.id}"


class Visit(Base):
    __tablename__ = "visit_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP,
        default=datetime.utcnow
    )

    executor_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("worker_table.id"))
    order_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("order_table.id"))
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("customer_table.id"))
    where_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("store_table.id"))

    executor: Mapped["Worker"] = relationship()
    order: Mapped["Order"] = relationship()
    author: Mapped["Customer"] = relationship()
    where: Mapped["Store"] = relationship()

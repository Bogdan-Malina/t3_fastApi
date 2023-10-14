from datetime import datetime

import sqlalchemy
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List


from database.database import Base


from sqlalchemy.orm import validates


class Statuses(enum.Enum):
    started = "started"
    ended = "ended"
    in_process = "in_process"
    awaiting = "awaiting"
    canceled = "canceled"

    @staticmethod
    def get_status():
        statuses = list(map(lambda c: c.value, Statuses))
        return statuses


customer_store = sqlalchemy.Table(
    "customer_store",
    Base.metadata,
    sqlalchemy.Column(
        "customer_id",
        sqlalchemy.ForeignKey("customer_table.id"),
        primary_key=True,
        nullable=False,
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

    workers: Mapped[List["Worker"]] = relationship(
        secondary=worker_store,
        back_populates="stores"
    )
    customers: Mapped[List["Customer"]] = relationship(
        secondary=customer_store,
        back_populates="stores"
    )

    orders: Mapped[List["Order"]] = relationship(
        backref="where",
        cascade="all, delete"
    )
    visits: Mapped[List["Visit"]] = relationship(
        backref="where",
        cascade="all, delete"
    )

    def __str__(self):
        return self.name


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(255))
    phone_number: Mapped[str] = mapped_column(
        sqlalchemy.String(255),
        unique=True
    )

    stores: Mapped[List["Store"]] = relationship(
        secondary=customer_store,
        back_populates="customers",
    )

    orders: Mapped[List["Order"]] = relationship(
        backref="author",
        cascade="all, delete"
    )
    visits: Mapped[List["Visit"]] = relationship(
        backref="author",
        cascade="all, delete"
    )

    def __str__(self):
        return self.name


class Worker(Base):
    __tablename__ = "worker_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(255))
    phone_number: Mapped[str] = mapped_column(
        sqlalchemy.String(255),
        unique=True
    )

    stores: Mapped[List["Store"]] = relationship(
        secondary=worker_store,
        back_populates="workers"
    )

    orders: Mapped[List["Order"]] = relationship(
        backref="executor",
        cascade="all, delete"
    )
    visits: Mapped[List["Visit"]] = relationship(
        backref="executor",
        cascade="all, delete"
    )

    def __str__(self):
        return self.name


class Order(Base):
    __tablename__ = "order_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP,
        default=datetime.utcnow
    )
    close_date: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP,
        default=datetime.utcnow
    )
    status: Mapped[sqlalchemy.Enum] = mapped_column(
        sqlalchemy.Enum(Statuses),
        default=Statuses.started
    )

    where_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("store_table.id")
    )
    author_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("customer_table.id")
    )
    executor_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("worker_table.id")
    )

    visit: Mapped["Visit"] = relationship(
        backref="order",
        cascade="all, delete"
    )

    @validates("author_id")
    def validate_author(self, key, author_id):
        customers = self.where.customers
        author = self.author
        if author not in customers:
            raise ValueError("Author error")
        return author_id

    @validates("executor_id")
    def validate_executor(self, key, executor_id):
        workers = self.where.workers
        worker = self.executor
        if worker not in workers:
            raise ValueError("Executor error")
        return executor_id

    def __str__(self):
        return f"{self.id}"


class Visit(Base):
    __tablename__ = "visit_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(
        sqlalchemy.TIMESTAMP,
        default=datetime.utcnow,
    )

    executor_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("worker_table.id")
    )
    order_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("order_table.id")
    )
    author_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("customer_table.id")
    )
    where_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("store_table.id")
    )

    @validates("executor_id")
    def validate_executor(self, key, executor_id):
        print(executor_id)
        if executor_id != self.order.executor_id:
            raise ValueError("Executor error")
        return executor_id

    @validates("author_id")
    def validate_author(self, key, author_id):
        if author_id != self.order.author_id:
            raise ValueError("Author error")
        return author_id

    @validates("where_id")
    def validate_where(self, key, where_id):
        if where_id != self.order.where_id:
            raise ValueError("Where error")
        return where_id

    def __str__(self):
        return f"{self.id}"

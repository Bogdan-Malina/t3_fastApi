from database.models import models
from database.database import engine
from sqlalchemy.orm import Session
import random

NAMES_USERS = [
    "Hop",
    "Cooper",
    "Kyle",
    "Beck",
    "Slade",
    "Hop",
    "Cooper",
    "Kyle",
    "Beck",
    "Slade",
    "Hop",
    "Cooper",
    "Kyle",
    "Beck",
    "Slade"
]
SURNAMES_USERS = [
    "Griffin",
    "Terry",
    "Banks",
    "Terrell",
    "Lyons",
    "Lowery",
    "Walter",
    "Boone",
    "Lynch",
    "Soto",
    "Calderon",
    "Hopper",
    "Foley",
    "Faulkner",
    "Hubbard"
]

NAMES_STORES = [
    "Auctor",
    "A",
    "PC",
    "Mauris",
    "Lacus",
    "Velit",
    "Cras",
    "Consulting",
    "Aliquam",
    "Corporation",
    "Nulla",
    "Consulting",
    "Risus",
    "Inc.",
    "Quis",
    "Pede",
    "Praesent",
    "PC",
    "Vestibulum",
    "Fermentum",
    "Neque",
    "Foundation",
    "Hendrerit",
    "LLC",
    "Cum",
    "Sociis",
    "Tristique",
    "Industries",
    "Corporation",
]


def create_stores():
    name = (
        f"{random.choice(NAMES_STORES)} "
        f"{random.choice(NAMES_STORES)}"
    )
    store_create = models.Store(
        name=name,
    )
    return store_create


def create_user(store, role_model):
    name = (
        f"{random.choice(NAMES_USERS)}"
        f" {random.choice(SURNAMES_USERS)}"
    )
    phone_number = random.randint(100000, 999999)
    user = role_model(
        name=name,
        phone_number=phone_number,
        stores=[store]
    )
    return user


def create_orders(store):
    executor = random.choice(store.workers)
    customer = random.choice(store.customers)
    if customer and executor:
        order_create = models.Order(
            where=store,
            author=customer,
            executor=executor
        )
        return order_create


def create_visits(order):
    visit = models.Visit(
        where=order.where,
        author=order.author,
        executor=order.executor,
        order=order
    )
    return visit


with Session(engine) as session:
    for i in range(75):
        try:
            session.add(create_stores())
            session.commit()
        except Exception:
            continue
    stores_list = session.query(models.Store).all()
    for i in range(300):
        try:
            store_worker = random.choice(stores_list)
            session.add(create_user(store_worker, models.Worker))
            session.commit()
        except Exception:
            continue
    for i in range(300):
        try:
            store_customer = random.choice(stores_list)
            session.add(create_user(store_customer, models.Customer))
            session.commit()
        except Exception:
            continue
    stores_list = session.query(models.Store).all()
    for i in range(200):
        try:
            store_order = random.choice(stores_list)
            session.add(create_orders(store_order))
            session.commit()
        except Exception:
            continue
    orders_list = session.query(models.Order).all()
    for i in range(100):
        try:
            order_visit = orders_list[i]
            session.add(create_visits(order_visit))
            session.commit()
        except Exception:
            continue

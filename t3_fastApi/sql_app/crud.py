from sqlalchemy.orm import Session

# import sql_app.models as models
# import sql_app.schemas as schemas
from . import models
from . import schemas


# def get_stores(
#         phone_number: str,
#         db: Session,
#         skip: int = 0,
#         limit: int = 100
#     ):
#     return db.query(models.Store).offset(skip).limit(limit).all()

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def create_store(db: Session, store: schemas.StoreCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    db_store = models.Store(name=store.name)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def get_workers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Worker).offset(skip).limit(limit).all()


def create_worker(db: Session, worker: schemas.WorkerCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    db_worker = models.Worker(
        name=worker.name,
        phone_number=worker.phone_number,
        store_id=worker.store_id
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
def get_stores_by_phone(phone, db, skip, limit):
    worker = (
        db.query(models.Worker)
        .filter(models.Worker.phone_number == phone)
        .first()
    )
    if worker:
        stores = worker.stores
        return stores
    else:
        return []


def get_orders_by_phone(phone, db, skip, limit):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.phone_number == phone)
        .first()
    )
    if customer:
        orders = (
            db.query(models.Order)
            .filter(models.Order.author == customer)
            .all()
        )
        return orders
    else:
        return []


def post_order_by_phone(phone, db, order):
    try:
        author = (
            db.query(models.Customer)
            .filter(models.Customer.phone_number == phone)
            .first()
        )
        if not author:
            return []
        store = (
            db.query(models.customer_store)
            .filter(
                models.customer_store.columns.store_id == author.id,
                models.customer_store.columns.customer_id == order.where_id,
            )
            .first()
        )
        print(store)
        if not store:
            return []
        executor = (
            store.workers.
            filter(models.Worker.id == order.executor_id)
            .first()
        )
        print(executor, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        db_order = models.Order(
            where=store,
            author=author,
            executor=executor
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except BaseException as e:
        print(e)
        return {"error": f"{e}"}

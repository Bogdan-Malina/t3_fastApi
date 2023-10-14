from datetime import datetime
from fastapi import HTTPException
from database.models import models


def get_customer_by_phone(phone, db):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.phone_number == phone)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=400, detail="Phone not found")
    return customer


def get_stores_by_phone(phone, db):
    worker = (
        db.query(models.Worker)
        .filter(models.Worker.phone_number == phone)
        .first()
    )
    if worker:
        stores = worker.stores
        return stores
    else:
        raise HTTPException(status_code=400, detail="Stores not found")


def get_orders_by_phone(phone, db):
    customer = get_customer_by_phone(phone, db)
    if customer:
        orders = (
            db.query(models.Order)
            .filter(models.Order.author == customer)
            .all()
        )
        return orders
    else:
        raise HTTPException(status_code=400, detail="Orders not found")


def post_order_by_phone(phone, db, order):
    author = get_customer_by_phone(phone, db)
    store = (
        db.query(models.Store)
        .filter(
            models.Store.id == order.where_id
        )
        .first()
    )
    if not store:
        raise HTTPException(status_code=400, detail="Store not found")
    store_valid = (
        db.query(models.customer_store)
        .filter(
            models.customer_store.columns.store_id == store.id,
            models.customer_store.columns.customer_id == author.id,
        )
        .first()
    )
    if not store_valid:
        raise HTTPException(status_code=400, detail="Store is not valid")
    executor = (
        db.query(models.Worker).
        filter(models.Worker.id == order.executor_id)
        .first()
    )
    if not executor:
        raise HTTPException(status_code=400, detail="Executor not found")
    executor_valid = (
        db.query(models.worker_store)
        .filter(
            models.worker_store.columns.store_id == store.id,
            models.worker_store.columns.worker_id == executor.id,
        )
        .first()
    )
    if not executor_valid:
        raise HTTPException(status_code=400, detail="Executor is not valid")
    db_order = models.Order(
        where=store,
        author=author,
        executor=executor,
        close_date=order.close_date,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order_by_phone(phone, db, order):
    author = get_customer_by_phone(phone, db)
    deleted_order = (
        db.query(models.Order)
        .filter(
            models.Order.id == order.id,
            models.Order.author == author
        ).first()
    )
    if not deleted_order:
        raise HTTPException(status_code=400, detail="Order not found")
    db.delete(deleted_order)
    db.commit()
    return HTTPException(status_code=200, detail="Order deleted")


def put_order_by_phone(phone, db, order):
    author = get_customer_by_phone(phone, db)
    updated_order = (
        db.query(models.Order)
        .filter(
            models.Order.id == order.id,
            models.Order.author == author
        ).first()
    )
    if not updated_order:
        raise HTTPException(status_code=400, detail="Order not found")

    updated_order.status = order.status
    db.commit()
    return HTTPException(status_code=200, detail="Order updated")


def get_visits_by_phone(phone, db):
    author = get_customer_by_phone(phone, db)
    visits = (
        db.query(models.Visit)
        .filter(models.Visit.author == author)
        .all()
    )
    if not visits:
        raise HTTPException(status_code=400, detail="Visits not found")
    return visits


def post_visits_by_phone(phone, db, visit):
    author = get_customer_by_phone(phone, db)
    visit_validate = (
        db.query(models.Visit)
        .filter(
            models.Visit.order_id == visit.order_id
        ).first()
    )
    if visit_validate:
        if visit_validate.author != author:
            raise HTTPException(status_code=400, detail="Visit not found")
        raise HTTPException(status_code=400, detail="Visit already exists")

    order = (
        db.query(models.Order)
        .filter(
            models.Order.id == visit.order_id
        )
        .first()
    )

    if not order or order.author != author:
        raise HTTPException(status_code=400, detail="Order not found")
    if order.close_date > datetime.utcnow():
        raise HTTPException(status_code=400, detail="Error close date")

    db_visit = models.Visit(
        executor=order.executor,
        order=order,
        author=author,
        where=order.where,
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def delete_visit_by_phone(phone, db, visit):
    author = get_customer_by_phone(phone, db)
    deleted_visit = (
        db.query(models.Visit)
        .filter(
            models.Visit.id == visit.id,
            models.Visit.author == author
        ).first()
    )
    if not deleted_visit:
        raise HTTPException(status_code=400, detail="Visit not found")
    db.delete(deleted_visit)
    db.commit()
    return HTTPException(status_code=200, detail="Visit deleted")

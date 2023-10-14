from flask import Flask
from flask_admin import Admin

from admin.models.admin_models import WorkerView, CustomerView, StoreView, OrderView, VisitView
from database.models.models import Worker, Store, Customer, Order, Visit


def create_flask(db):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "asdf"
    admin = Admin(
        app,
        url="/",
        name="Админка",
        template_mode="bootstrap4"
    )
    admin.add_view(WorkerView(Worker, db, name="Работник"))
    admin.add_view(CustomerView(Customer, db, name="Заказчик"))
    admin.add_view(StoreView(Store, db, name="Торговая точка"))
    admin.add_view(OrderView(Order, db, name="Заказ"))
    admin.add_view(VisitView(Visit, db, name="Посещение"))

    return admin.app

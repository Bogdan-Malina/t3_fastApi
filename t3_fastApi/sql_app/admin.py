from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sql_app.models import Worker, Store, Customer, Order, Visit


class WorkerView(ModelView):
    column_list = ('id', 'name', 'phone_number', 'stores')
    column_searchable_list = ('name', 'phone_number')
    column_filters = ('id', 'name')


class StoreView(ModelView):
    column_list = ('id', 'name', 'workers', 'customers')
    column_searchable_list = ('id', 'name')
    column_filters = ('id', 'name')


class CustomerView(ModelView):
    column_list = ('id', 'name', 'phone_number', 'stores')
    column_searchable_list = ('name', 'phone_number')
    column_filters = ('id', 'name')


class OrderView(ModelView):
    column_list = (
        "id",
        "create_date",
        "close_date",
        "status",
        "where",
        "author",
        "executor"
    )
    column_searchable_list = ("id", "status")
    column_filters = ("id", "status")


class VisitView(ModelView):
    column_list = (
        "id",
        "create_date",
        "executor",
        "order",
        "author",
        "where",
    )
    column_searchable_list = ("id", "create_date")
    column_filters = ("id", "create_date")

 
def create_flask(db):
    print(db)
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
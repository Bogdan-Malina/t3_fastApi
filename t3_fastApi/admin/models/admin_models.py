from flask_admin.contrib.sqla import ModelView


class WorkerView(ModelView):
    column_list = ("id", "name", "phone_number", "stores")
    column_searchable_list = ("name", "phone_number")
    column_filters = ("name", "phone_number")


class StoreView(ModelView):
    column_list = ("id", "name", "workers", "customers")
    column_searchable_list = ("id", "name")
    column_filters = ("id", "name")


class CustomerView(ModelView):
    column_list = ("id", "name", "phone_number", "stores")
    column_searchable_list = ("name", "phone_number")
    column_filters = ("name", "phone_number")


class OrderView(ModelView):
    column_list = (
        "id",
        "create_date",
        "close_date",
        "status",
        # "where",
        # "author",
        # "executor"
    )
    column_searchable_list = ("id", "create_date")
    column_filters = ("id", "create_date", "status")


class VisitView(ModelView):
    column_list = (
        "id",
        "create_date",
        # "executor",
        # "order",
        # "author",
        # "where",
    )
    column_searchable_list = ("id", "create_date")
    column_filters = ("id", "create_date",
                      # "author"
                      )

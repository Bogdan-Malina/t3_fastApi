from fastapi import FastAPI

from database.models import models
from database.database import engine

from api.routers import stores, visits, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(stores.router)
app.include_router(orders.router)
app.include_router(visits.router)

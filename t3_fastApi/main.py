from fastapi.middleware.wsgi import WSGIMiddleware
from database.database import SessionLocal
from admin.create_admin import create_flask
from api.app import app


app = app
app.mount("/admin", WSGIMiddleware(create_flask(SessionLocal())))

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware

from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from sql_app.admin import create_flask

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/admin", WSGIMiddleware(create_flask(SessionLocal())))


# Dependency
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()



@app.get("/store/", response_model=list[schemas.Store])
def read_store(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stores = crud.get_stores(db, skip=skip, limit=limit)
    return stores


@app.post("/store/", response_model=schemas.Store)
def create_user(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    # db_store = crud.get_user_by_email(db, email=user.email)
    # if db_store:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_store(db=db, store=store)

@app.get("/worker/", response_model=list[schemas.Worker])
def read_worker(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    worker = crud.get_workers(db, skip=skip, limit=limit)
    return worker


@app.post("/worker/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    # db_store = crud.get_user_by_email(db, email=user.email)
    # if db_store:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_worker(db=db, worker=worker)


# @app.get("/admin/")
# def get_admin(db: Session = Depends(get_db)):
#     pass




@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

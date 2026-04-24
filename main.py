from fastapi import FastAPI
from database import engine, Base
import models.role
import models.user
from routers import users

app = FastAPI()

app.include_router(users.router)

Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from database import engine, Base
import models.role
import models.user

app = FastAPI()

Base.metadata.create_all(bind=engine)
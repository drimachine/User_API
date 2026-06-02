from fastapi import FastAPI
from database import engine, Base
import models.role
import models.user
from routers import users
from middlewares.user_id import user_id_middleware
from middlewares.logs import logs
import uvicorn

app = FastAPI()

app.include_router(users.router)
app.middleware("http")(logs)
app.middleware("http")(user_id_middleware)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
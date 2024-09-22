from fastapi import FastAPI

from . import database as db
from .goods.api import router as goods_router

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.include_router(prefix="/goods", router=goods_router)

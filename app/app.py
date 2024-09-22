from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database as db
from .goods.api import router as goods_router

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(prefix="/api/goods", router=goods_router)

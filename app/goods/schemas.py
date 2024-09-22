from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint


class GoodsCreate(BaseModel):
    sku_id: str
    name: str
    category: str
    amount: int
    avg_cart: Optional[float]
    dt: Optional[conint(ge=0, le=13)]
    trigger: Optional[float]
    shelve: str


class Goods(BaseModel):
    sku_id: str
    name: str
    category: str
    amount: int
    avg_cart: Optional[float]
    dt: Optional[conint(ge=0, le=13)]
    trigger: Optional[float]
    shelve: str

    class Config:
        orm_mode = True

from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.goods.models import Goods as GoodsModel
from app.model import predict

from . import crud
from .schemas import Goods, GoodsCreate

router = APIRouter()


@router.post("/", response_model=Goods)
def create_goods(goods: GoodsCreate, db: Session = Depends(get_db)):
    return crud.create_goods(db=db, goods=goods)


@router.get("/{sku_id}", response_model=Goods)
def read_goods_by_sku(sku_id: str, db: Session = Depends(get_db)):
    db_goods = crud.get_goods_by_sku(db=db, sku_id=sku_id)
    if db_goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    return db_goods


@router.get("/shelve/{shelve}", response_model=list[Goods])
def read_goods_by_shelve(shelve: str, db: Session = Depends(get_db)):
    db_goods = crud.get_goods_by_shelve(db=db, shelve=shelve)
    return db_goods


@router.put("/{sku_id}/amount", response_model=Goods)
def update_goods_amount_and_trigger(
    sku_id: str, new_amount: int, db: Session = Depends(get_db)
):
    db_goods = crud.get_goods_by_sku(db=db, sku_id=sku_id)

    if db_goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")

    input_data = pd.DataFrame(
        {
            "sku_id": [db_goods.sku_id],
            "name": [db_goods.name],
            "category": [db_goods.category],
            "amount": [new_amount],
            "avg_cart": [db_goods.avg_cart],
            "t_expiery": [db_goods.t_expiery],
            "stocktaking_time": [db_goods.stocktaking_time],
            "dt": [db_goods.dt],
        }
    )

    predicted_trigger = predict(input_data).data[0]

    db_goods.amount = new_amount
    db_goods.trigger = predicted_trigger

    db.commit()
    db.refresh(db_goods)

    return db_goods


@router.get("/", response_model=list[Goods])
def read_all_goods(db: Session = Depends(get_db)):
    return crud.get_all_goods(db=db)


@router.get("/shelves/", response_model=list[dict])
def read_all_shelves(db: Session = Depends(get_db)):
    shelves_with_avg_trigger = crud.get_all_shelves_with_avg_trigger(db=db)

    return [
        {"shelve": shelve, "avg_trigger": avg_trigger}
        for shelve, avg_trigger in shelves_with_avg_trigger
    ]


@router.put("/dt/{new_dt}", response_model=list[Goods])
def update_all_goods_dt(new_dt: int, db: Session = Depends(get_db)):
    if new_dt < 0 or new_dt > 13:
        raise HTTPException(status_code=400, detail="dt must be between 0 and 13")

    all_goods = db.query(GoodsModel).all()

    if not all_goods:
        raise HTTPException(status_code=404, detail="No goods found")

    updated_goods = []

    for item in all_goods:
        item.dt = new_dt

        input_data = pd.DataFrame(
            {
                "sku_id": [item.sku_id],
                "name": [item.name],
                "category": [item.category],
                "amount": [item.amount],
                "avg_cart": [item.avg_cart],
                "t_expiery": [item.t_expiery],
                "stocktaking_time": [item.stocktaking_time],
                "dt": [new_dt],
            }
        )

        predicted_trigger = predict(input_data).data[0]

        item.trigger = predicted_trigger

        updated_goods.append(item)

    db.commit()

    return updated_goods

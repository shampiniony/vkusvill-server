from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

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
def update_goods_amount(sku_id: str, new_amount: int, db: Session = Depends(get_db)):
    db_goods = crud.update_goods_amount(db=db, sku_id=sku_id, new_amount=new_amount)
    if db_goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    return db_goods


@router.get("/", response_model=list[Goods])
def read_all_goods(db: Session = Depends(get_db)):
    return crud.get_all_goods(db=db)


@router.get("/shelves/", response_model=list[str])
def read_all_shelves(db: Session = Depends(get_db)):
    shelves = crud.get_all_shelves(db=db)
    return [shelve[0] for shelve in shelves]

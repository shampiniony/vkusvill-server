from sqlalchemy import Column, Float, Integer, String, Text

from app.database import Base


class Goods(Base):
    __tablename__ = "goods"

    sku_id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(Text)
    amount = Column(Integer)
    avg_cart = Column(Float)
    t_expiery = Column(Integer, default=100)
    stocktaking_time = Column(Integer, default=30)
    dt = Column(Integer)
    trigger = Column(Float)
    shelve = Column(String)

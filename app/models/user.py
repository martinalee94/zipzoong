from app.db.mysql import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Seller(Base):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uniq_num = Column(String(36), unique=True, index=True)
    nickname = Column(String(20), null=True)
    phone = Column(String(11), null=True)

    house = relationship("House", back_populates="house")
    # https://fastapi.tiangolo.com/tutorial/sql-databases/ 


class Agent(Base):
    __tablename__ = "agent"

    id = Column(Integer, primary_ey=True, autoincrement=True)
    uniq_num = Column(String(32), unique=True, index=True)

    bid = relationship("HouseBidInfo", back_populates="bid")

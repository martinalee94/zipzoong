from typing import Union

from app.db.mysql import Base
from sqlalchemy import (TIMESTAMP, Column, DateTime, FetchedValue, ForeignKey,
                        Integer, SmallInteger, String)
from sqlalchemy.orm import relationship


class House(Base):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(4), nullable=True, index=True)
    contract_type = Column(String(4), nullable=True, index=True)
    sell_price = Column(Integer, nullable=True)
    charter_rent_price = Column(Integer, nullable=True)
    monthly_rent_price = Column(Integer, nullable=True)
    deposit_rent_price = Column(Integer, nullable=True)
    full_addr = Column(String(256))
    sido_addr = Column(String(32), nullable=True)
    gungu_addr = Column(String(32), nullable=True)
    street_addr = Column(String(128), nullable=True)
    detail_addr = Column(String(256), nullable=True)
    postal_code = Column(String(6), nullable=True)
    created_date = Column(TIMESTAMP(), server_default=FetchedValue())
    seller_id = relationship("Seller", ForeignKey("seller.id"))

    seller = relationship("Seller", back_populates="house")
    option = relationship("HouseDetail", back_populates="house")
    images = relationship("HouseImage", back_populates="house")
    bid = relationship("HouseBidInfo", back_populates="house")


class HouseDetail(Base):
    __tablename__ = "house_option"

    id = Column(Integer, primary_key=True, autoincrement=True)
    floor = Column(SmallInteger())
    rooms = Column(SmallInteger())
    washrooms = Column(SmallInteger())
    created_date = Column(TIMESTAMP(), server_default=FetchedValue())
    house_id = Column(Integer, ForeignKey("house.id"))

    house = relationship("House", back_populates="option")


class HouseImage(Base):
    __tablename__ = "house_image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(256))
    filename = Column(String(256))
    size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    image_type = Column(SmallInteger)
    created_date = Column(TIMESTAMP(), server_default=FetchedValue())
    house_id = Column(Integer, ForeignKey("house.id"))

    house = relationship("House", back_populates="images")


class HouseBidInfo(Base):
    __tablename__ = "house_bid_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bid_price = Column(Integer)
    is_contacted = Column(SmallInteger, default=0)
    is_chosen = Column(SmallInteger, default=0)
    kind_point = Column(SmallInteger)
    speed_point = Column(SmallInteger)
    cost_point = Column(SmallInteger)
    time_point = Column(SmallInteger)
    quality_point = Column(SmallInteger)
    house_id = Column(Integer, ForeignKey("House.id"))
    agent_id = Column(Integer, ForeignKey("Agent.id"))

    house = relationship("House", back_populates="bid")
    agent = relationship("Agent", back_popluates="bid")

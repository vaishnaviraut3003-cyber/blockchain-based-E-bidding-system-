from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    wallet_address = Column(String, unique=True, nullable=True)


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    starting_price = Column(Float, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"))
    tender_id = Column(Integer, ForeignKey("tenders.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    bid_hash = Column(String, nullable=False)
    blockchain_tx_hash = Column(String, nullable=True)
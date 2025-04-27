from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String)

    vpn_key = relationship("VPNKey", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="raise")
    subscription = relationship("Subscription", back_populates="user", uselist=False, lazy="raise")
    orders = relationship("Order", back_populates="user")

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    vpn_key_id = Column(Integer, ForeignKey("vpn_keys.id", ondelete="CASCADE"), unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)

    vpn_key = relationship("VPNKey", back_populates="subscription", lazy="raise")
    user = relationship("User", back_populates="subscription", lazy="raise")

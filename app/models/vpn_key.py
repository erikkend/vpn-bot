from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class VPNKey(Base):
    __tablename__ = 'vpn_keys'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    full_key_data = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    key_uuid = Column(String, default=None)
    key_email = Column(String, default=None)
    key_sub_id = Column(String, default=None)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"))
    
    user = relationship("User", back_populates="vpn_key", lazy="raise")
    subscription = relationship("Subscription", back_populates="vpn_key", uselist=False, lazy="raise")
    server = relationship("Server", back_populates="vpn_key", uselist=False, lazy="raise")
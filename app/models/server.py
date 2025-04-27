from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    server_ip = Column(String)
    region = Column(String)
    panel_port = Column(Integer)
    panel_webpath = Column(String)
    panel_username = Column(String)
    panel_password = Column(String)
    is_active = Column(Boolean, default=False)
    workload = Column(Integer)

    vpn_key = relationship("VPNKey", back_populates="server", uselist=False, lazy="raise")
    
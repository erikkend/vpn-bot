from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from enum import Enum as PyEnum
from dateutil.relativedelta import relativedelta

class OrderStatus(PyEnum):
    PAID = "paid"
    PAID_OVER = "paid_over"
    WRONG_AMOUNT = "wrong_amount"
    PROCESS = "process"
    CONFIRM_CHECK = "confirm_check"
    WRONG_AMOUNT_WAITING = "wrong_amount_waiting"
    CHECK = "check"
    FAIL = "fail"
    CANCEL = "cancel"
    SYSTEM_FAIL = "system_fail"
    REFUND_PROCESS = "refund_process"
    REFUND_FAIL = "refund_fail"
    REFUND_PAID = "refund_paid"
    LOCKED = "locked"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    order_uuid = Column(String, unique=True, nullable=True)
    amount = Column(Numeric(10,2), nullable=True)
    currency = Column(String, nullable=False)
    month_count = Column(Integer, nullable=False)
    server_region = Column(String, nullable=False)
    
    status = Column(Enum(OrderStatus), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    paid_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="orders")

    @property
    def is_expired(self):
        return self.expires_at < datetime.now()

    @property
    def is_paid(self):
        return self.status in {OrderStatus.PAID, OrderStatus.PAID_OVER}

    @staticmethod
    def generate_expire_time():
        return datetime.now() + relativedelta(minutes=15)

    def __str__(self):
        return f"{self.id}: {self.order_uuid}"
    
    
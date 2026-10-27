from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CallRecord(Base):
    __tablename__ = "call_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    caller_name: Mapped[str] = mapped_column(String(255))
    caller_number: Mapped[str] = mapped_column(String(32), index=True)
    receiver_number: Mapped[str] = mapped_column(String(32))
    city: Mapped[str] = mapped_column(String(150), index=True)
    call_direction: Mapped[bool] = mapped_column(Boolean)
    call_status: Mapped[bool] = mapped_column(Boolean)
    call_duration: Mapped[int] = mapped_column(Integer)
    call_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    call_start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )
    call_end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
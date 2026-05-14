from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, DateTime, Numeric, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base

class AlertDirection(str, enum.Enum):
    ABOVE = "above"   # цена выросла выше порога
    BELOW = "below"   # цена упала ниже порога

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    coin_id: Mapped[str] = mapped_column(String(100))
    coin_symbol: Mapped[str] = mapped_column(String(20))
    target_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    direction: Mapped[AlertDirection] = mapped_column(Enum(AlertDirection))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="alerts")
    history: Mapped[list["AlertHistory"]] = relationship(back_populates="alert", cascade="all, delete-orphan")

class AlertHistory(Base):
    __tablename__ = "alert_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id", ondelete="CASCADE"), index=True)
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    price_at_trigger: Mapped[Decimal] = mapped_column(Numeric(20, 8))

    alert: Mapped["Alert"] = relationship(back_populates="history")
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, ForeignKey, DateTime, Numeric, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(100), default="Мой портфель")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="portfolios")
    assets: Mapped[list["PortfolioAsset"]] = relationship(back_populates="portfolio", cascade="all, delete-orphan")

class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "coin_id", name="uq_portfolio_coin"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), index=True)
    coin_id: Mapped[str] = mapped_column(String(100))
    coin_symbol: Mapped[str] = mapped_column(String(20))
    coin_name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[Decimal] = mapped_column(Numeric(30, 18))  # количество монет
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="assets")
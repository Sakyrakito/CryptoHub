from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "coin_id", name="uq_user_coin"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    coin_id: Mapped[str] = mapped_column(String(100))   # "bitcoin", "ethereum" — id из CoinGecko
    coin_symbol: Mapped[str] = mapped_column(String(20)) # "BTC", "ETH"
    coin_name: Mapped[str] = mapped_column(String(100))  # "Bitcoin"
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="favorites")
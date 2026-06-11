from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    stock_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    reserved_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    # Calculates the available quantity from database
    @property
    def available_quantity(self) -> int:
        return self.stock_quantity - self.reserved_quantity

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
    quantity: Mapped[int | None] = mapped_column(
        Integer, nullable=False, default=0
    )
    reserved_quantity: Mapped[int | None] = mapped_column(
        Integer, nullable=False, default=0
    )

    # Calculates the available quantity from database
    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity

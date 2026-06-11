# SQLAlchemy (Database) Models for order service

from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.ordering_service.enums import OrderStatus

# Nullable explicitly for important business fields
# Can imply nullable via typehints with [type | None]


# Order Table
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    order_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

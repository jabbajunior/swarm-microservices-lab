from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.ordering_service.enums import OrderStatus


class OrderBase(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


# Order - User supplies to Create
class OrderCreate(OrderBase):
    pass


# Order Responses
class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int

    total_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    user_id: int | None


# Purposefully Omitting product_id as the logic can get quite messy
class OrderUpdate(BaseModel):
    quantity: int | None = Field(default=None, gt=0)
    status: OrderStatus | None = Field(default=None)

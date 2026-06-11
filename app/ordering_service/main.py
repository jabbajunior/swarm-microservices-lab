from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.init_db import init_db
from app.ordering_service import models
from app.ordering_service.enums import OrderStatus
from app.ordering_service.models import Order
from app.ordering_service.schemas import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from app.product_catalog.models import Product

init_db()
app = FastAPI()


# Helper Methods
def _get_order_or_404(
    order_id: int, db: Annotated[Session, Depends(get_db)]
) -> models.Order:

    result = db.execute(
        select(models.Order).where(models.Order.id == order_id)
    )

    order = result.scalars().first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


## Create an order
@app.post(
    "/api/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: OrderCreate, db: Annotated[Session, Depends(get_db)]
) -> models.Order:

    # Grabs the matching product and calculates price based on quantity purchased
    result = db.execute(select(Product).where(Product.id == order.product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    total_price = product.price * order.order_quantity

    new_order = models.Order(
        product_id=order.product_id,
        order_quantity=order.order_quantity,
        total_price=total_price,
        status=OrderStatus.PENDING,
        user_id=None,  # TODO Update later to reflect who placed the order
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


## Read
# Read all orders
@app.get(
    "/api/orders",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def list_orders(db: Annotated[Session, Depends(get_db)]) -> list[models.Order]:

    result = db.execute(select(models.Order))
    orders = list(result.scalars().all())

    return orders


@app.get(
    "/api/orders/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order(
    order_id: int, db: Annotated[Session, Depends(get_db)]
) -> models.Order:

    order = _get_order_or_404(order_id, db)

    return order


## Update
@app.patch(
    "/api/orders/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def update_order_partial(
    order_id: int,
    updated_order: OrderUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Order:

    order = _get_order_or_404(order_id, db)
    update_data = updated_order.model_dump(exclude_unset=True)

    #  Ensures order_quantity is not None
    if "order_quantity" in update_data:
        # Find the matching product
        result = db.execute(
            select(Product).where(Product.id == order.product_id)
        )
        product = result.scalars().first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Recalculate Price
        order.total_price = product.price * update_data["order_quantity"]

    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


## Delete
@app.delete(
    "/api/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(order_id: int, db: Annotated[Session, Depends(get_db)]):

    order = _get_order_or_404(order_id, db)

    db.delete(order)
    db.commit()

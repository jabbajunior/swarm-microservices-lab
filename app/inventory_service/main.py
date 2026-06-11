from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.init_db import init_db
from app.inventory_service import models
from app.inventory_service.models import Inventory
from app.inventory_service.schemas import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)

init_db()
app = FastAPI()

## TODO LATER enforce typehints for return values


# Helper Methods
def _get_inventory_item_or_404(
    inventory_id: int, db: Session
) -> models.Inventory:

    result = db.execute(
        select(models.Inventory).where(models.Inventory.id == inventory_id)
    )

    inventory_item = result.scalars().first()

    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found",
        )

    return inventory_item


# Create
@app.post(
    "/api/inventory/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory_item(
    inventory_item: InventoryCreate, db: Annotated[Session, Depends(get_db)]
) -> models.Inventory:

    result = db.execute(
        select(models.Inventory).where(
            models.Inventory.product_id == inventory_item.product_id
        )
    )

    existing_item = result.scalars().first()

    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inventory item already exists",
        )

    new_item = models.Inventory(
        product_id=inventory_item.product_id,
        stock_quantity=inventory_item.stock_quantity,
        reserved_quantity=inventory_item.reserved_quantity,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# Read entire inventory
@app.get(
    "/api/inventory",
    response_model=list[InventoryResponse],
    status_code=status.HTTP_200_OK,
)
def list_inventory(
    db: Annotated[Session, Depends(get_db)],
) -> list[models.Inventory]:

    result = db.execute(select(models.Inventory))
    inventory = list(result.scalars().all())

    return inventory


@app.get(
    "/api/inventory/{inventory_id}",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_inventory_item(
    inventory_id: int, db: Annotated[Session, Depends(get_db)]
) -> models.Inventory:

    inventory_item = _get_inventory_item_or_404(inventory_id, db)

    return inventory_item


## Partially Update an Individual Inventory Item
@app.patch(
    "/api/inventory/{inventory_id}",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK,
)
def update_inventory_item_partial(
    inventory_id: int,
    updated_item: InventoryUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Inventory:

    stored_item = _get_inventory_item_or_404(inventory_id, db)

    update_data = updated_item.model_dump(exclude_unset=True)

    new_quantity = update_data.get(
        "stock_quantity", stored_item.stock_quantity
    )
    new_reserved_quantity = update_data.get(
        "reserved_quantity", stored_item.reserved_quantity
    )

    if new_quantity < new_reserved_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity cannot be less than reserved quantity",
        )

    for field, value in update_data.items():
        setattr(stored_item, field, value)

    db.commit()
    db.refresh(stored_item)
    return stored_item


# Delete a single inventory item by ID
@app.delete(
    "/api/inventory/{inventory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_inventory_item(
    inventory_id: int, db: Annotated[Session, Depends(get_db)]
):
    stored_item = _get_inventory_item_or_404(inventory_id, db)

    db.delete(stored_item)
    db.commit()

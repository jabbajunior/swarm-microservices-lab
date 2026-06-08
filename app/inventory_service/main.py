from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.init_db import init_db
from app.inventory_service import models
from app.inventory_service.schemas import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)

app = FastAPI()

# Create


## TODO LATER enforce typehints for return values
# Read
@app.get(
    "/api/inventory",
    response_model=list[InventoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_inventory(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Inventory))
    inventory = result.scalars().all()

    return inventory


# Update

# Delete

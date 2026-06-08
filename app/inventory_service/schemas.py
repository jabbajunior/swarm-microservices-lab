from pydantic import BaseModel, ConfigDict, Field


# BaseInventory
class InventoryBase(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=0, ge=0)  # Total amount of inventory
    reserved_quantity: int = Field(
        default=0, ge=0
    )  # Amount of inventory reserved for customers


class InventoryCreate(InventoryBase):
    pass


# Inventory Response
class InventoryResponse(InventoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # Inventory ID
    available_quantity: int = Field(ge=0)  # Amount of available inventory left


class InventoryUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=0)
    reserved_quantity: int | None = Field(default=None, ge=0)

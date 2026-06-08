# Pydantic (DTO + Service) Models for product_catalog

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

# Dont repeat yourself

# Use typehints to enforce data types and **default values** when applicable


# A template not used by API directly, but allows other classes to inherit
# A shared schema
class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)  # Product Name
    description: str | None = Field(default=None)  # Product description.
    # Default value means its optional
    price: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2
    )  # Price per product


# Represents data an employee must provide when creating a product via API.
# Excludes server-generated fields such as id and timestamps.
class ProductCreate(ProductBase):
    pass


# Represents an update (can be partial).
# Fields are optional since client may only update one field
# Often does not inherit from ProductBase since that would require said inherited fields


class ProductUpdate(ProductBase):
    name: str | None = Field(
        default=None, min_length=1, max_length=128
    )  # Product Name
    description: str | None = Field(default=None)  # Product description.
    # Default value means its optional
    price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )  # Price per product


# Defines what the API returns. It includes server-managed fields.
class ProductResponse(ProductBase):
    # Can read database @property annotations as well
    model_config = ConfigDict(from_attributes=True)

    # adds these server generated fields to Client
    id: int

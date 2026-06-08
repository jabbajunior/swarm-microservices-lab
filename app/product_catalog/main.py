from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.init_db import init_db
from app.product_catalog import models
from app.product_catalog.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

init_db()
app = FastAPI()

# ALL APIS here are internally facing
# No direct user input


## Create
@app.post(
    "/api/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
# db: line explanation
# Signals to FastAPI to call get_db and return result as db
def create_product(
    product: ProductCreate, db: Annotated[Session, Depends(get_db)]
):
    # Ensure no duplicate products in catalog
    result = db.execute(
        select(models.Product).where(models.Product.name == product.name)
    )

    existing_product = result.scalars().first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists",
        )

    # New Product
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
    )

    # Add to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


## Read


# Get all products
@app.get(
    "/api/products",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
# db: Tells FastAPI to inject database into here
def get_products(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Product))
    products = result.scalars().all()

    return products


# Get a single product by ID
@app.get(
    "/api/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    # TODO should later guard against invalid queries such as -1 or Database queries (SQL Injection)
    # Query database for matching product ID
    result = db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )

    # Grabs first matching result or None if empty
    product = result.scalars().first()

    if product:
        return product

    # If no product, raise a 404 error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


## Partially Update an Individual Product
@app.patch(
    "/api/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
def update_product_partial(
    product_id: int,
    product_data: ProductUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )

    product = result.scalars().first()

    # Ensure do not update an invalid product_id
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Removes empty fields
    update_data = product_data.model_dump(exclude_unset=True)

    # Dynamically Sets fields to new ones
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


## Delete a single product by ID
@app.delete(
    "/api/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    # Query database for matching product ID
    result = db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )

    # Grabs first matching result or None if empty
    product = result.scalars().first()

    # If no product, raise a 404 error
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Delete the product
    db.delete(product)
    db.commit()

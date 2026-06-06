from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.product_catalog import models
from app.product_catalog.database import Base, engine, get_db
from app.product_catalog.schemas import ProductCreate, ProductResponse

# Create Tables if they do not already exist
Base.metadata.create_all(bind=engine)
app = FastAPI()


# Authorized API Section
# ----------------------


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
@app.get("/api/products", response_model=list[ProductResponse])
# db: Tells FastAPI to inject database into here
def get_products(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Product))
    products = result.scalars().all()

    return products


# Get a single product by ID
@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    # TODO should later guard against invalid queries such as -1 or Database queries (select all fomr *)
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


## Update

## Delete

# User-Facing API Section

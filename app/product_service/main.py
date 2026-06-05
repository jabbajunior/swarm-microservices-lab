from fastapi import FastAPI, HTTPException, status

from app.product_service.models import ProductCreate, ProductResponse

app = FastAPI()

products: list[dict] = [
    {"id": 1, "name": "Toothbrush", "price": 6},
    {"id": 2, "name": "Hairbrush", "price": 12},
    {"id": 3, "name": "Toilet Paper", "price": 9},
    {"id": 4, "name": "Lotion", "price": 7},
    {"id": 5, "name": "Bottle", "price": 11},
]


# Authorized API Section


## Create
@app.post(
    "/api/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate):
    new_id = max(p["id"] for p in products) + 1 if products else 1
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
    }
    products.append(new_product)
    return new_product


## Read


# Get all products
@app.get("/api/products", response_model=list[ProductResponse])
def get_products():
    return products


# Get a single product by ID
@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


## Update

## Delete

# User-Facing API Section

from fastapi import FastAPI, HTTPException, status

# from models import ProductCreate, ProductResponse

app = FastAPI()

products: list[dict] = [
    {
        "id": 1,
        "name": "Toothbrush",
        "price": 6
    },
    {
        "id": 2,
        "name": "Hairbrush",
        "price": 12
    },
    {
        "id": 3,
        "name": "Toilet Paper",
        "price": 9
    },
    {
        "id": 4,
        "name": "Lotion",
        "price": 7
    },
    {
        "id": 5,
        "name": "Bottle",
        "price": 11
    }
]


# Authorized API Section

## Create

## Read

# Get all products
@app.get("/api/products")
def get_products():
    return products


# Get a single product by ID
@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

## Update

## Delete



# User-Facing API Section

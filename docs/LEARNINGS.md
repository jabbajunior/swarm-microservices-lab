This doc is where I will put any insights or concepts learned.
At the end of each session, refine the learnings so that later we can extract value instead of
them just being ramblings.

# Pydantic

## BaseModel
This is essentially a data class from Spring where a class is serving as a template.

Are validated by pydantic so no need for explicit data validation
- Really useful

Can do
```python
class ProductCreate(ProductBase):
    pass
```

Would be a carbon copy of ProductBase that can be edited later

```python
class ProductResponse(ProductBase):
    # Allows pydantic to read from object notation (test.number) 
    # which is how databases store info
    model_config = ConfigDict(from_attributes=True) 
    
    product_id: int
    date_posted: str
```


Typical endpoint mapping:

  POST   /products       ProductCreate   -> ProductResponse
  GET    /products/{id}  no request body -> ProductResponse
  PATCH  /products/{id}  ProductUpdate   -> ProductResponse
  DELETE /products/{id}  no request body -> no body or ProductResponse

  This separation prevents clients from supplying fields they should not control:

  # Dangerous if used for creation:
  class Product(BaseModel):
      id: int
      is_active: bool
      created_at: datetime

  A client could then attempt to choose the database ID or creation timestamp.

  ProductBase inheritance is optional. Use it when it removes meaningful duplication, 
  but do not force every schema into an inheritance hierarchy. 
  
The important convention is having separate request and response schemas 
with appropriate fields and validation.


---
My perspective has shifted as if we are assuming that I am a company deploying this website, 
we need 2 types of APIs:

- Public facing API that the Website uses to serve content
- Private facing authorized API that employees use to edit content

Already learned this from Software Engineering Capstone, but this solidified this concept.
Much safer to use an API with data validation instead of doing manual edits that can 
bypass schema or validation. 

---

When importing from other classes, they need to be packages via `__init__.py` to be resolvable.

---

PyCharm is much heavier on PC resources on a remote server compared to vscode.

---

# Path Parameters
Variables embedded into a URL path. 

```python
/api/posts/{post_id}
```

FastAPI can validate these parameters via typehints 

---

I am liking the way FastAPI structures directories when compared to overly verbose spring.
I plan on following this schema:

```python
 Keep these concepts separate:

  - schemas.py: Pydantic API request and response formats.
  - models.py: SQLAlchemy database table mappings.
  - service.py: business logic.
  - routes.py: HTTP endpoints.
```
# Purpose

This document captures concepts, decisions, and implementation lessons learned
while building the project. The goal is to keep useful context in one place so
each session can end with clearer notes instead of scattered observations.

---

# Path Parameters

Path parameters are variables embedded directly in a URL path.

Example:

```python
http://localhost/api/posts/3
```
In this example, `3` is the ID of the specific post being requested.
<br></br>

In FastAPI, the route can define that value with braces:

```python
/api/posts/{post_id}
```

Then the function can use a type hint to tell FastAPI what kind of value it
expects:

```python
def get_post(post_id: int):
    ...
```

FastAPI automatically validates that path parameter. If someone passes an
invalid value, such as `/api/posts/not-a-number`, FastAPI returns an HTTP 422
response because the value cannot be converted to an `int`.

# Pydantic

Pydantic is a data validation library powered by type hints.

The main idea is that I can define the shape of data once, then FastAPI and
Pydantic can validate incoming request bodies and document the API from those
models.

## BaseModel

`BaseModel` is the class that Pydantic models inherit from. It feels similar to
a data class because it defines the fields that belong to a piece of data.

Example:

```python
class ProductBase(BaseModel):
    name: str
    price: Decimal
```

Pydantic uses the type hints to check that the incoming data has the expected
shape. If a required field is missing or has the wrong type, FastAPI can return
an HTTP 422 response automatically.

Models can also inherit from other models. This helps avoid repeating the same
fields when two API schemas are mostly the same.

Example:

```python
class ProductCreate(ProductBase):
    pass
```

In this example, `ProductCreate` has the same fields as `ProductBase`, but it
can still be expanded later if product creation needs its own fields.

## Validation

After hooking up `main.py` with the Pydantic product models, the API now has
automatic validation for missing fields and invalid data types. That makes the
app more robust without manually checking every request body.

Pydantic models also improve the generated FastAPI docs because the request and
response shapes become explicit.

---

# Miscellaneous Notes

## Public and Private APIs

Thinking about this like a company deploying a website makes the API split
clearer:

- Public-facing APIs serve product data to the website or customer clients.
- Private authorized APIs let employees create, update, or deactivate products.

I already learned this idea in Software Engineering Capstone, but this project
made it feel more concrete. It is safer to edit data through validated APIs than
through manual database changes that can bypass schema or request validation.

## Python Packages

When importing from other files, directories need an `__init__.py` file so
Python treats them as packages.

## Editor Notes

PyCharm has a larger footprint compared to VS Code when both are connected
to a remote server.

## FastAPI Project Structure

I like how FastAPI keeps structure lighter than Spring. For this project, I want
to keep these concepts separate:

- `schemas.py`: Pydantic API request and response formats
- `models.py`: SQLAlchemy database table mappings
- `service.py`: business logic
- `routes.py`: HTTP endpoints

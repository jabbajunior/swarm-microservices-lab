# TODO

Later edit python functions to support asynchronous calls

## Product Service Error Handling

Handle and test the common API failure cases instead of only testing happy
paths.

Bad URI or missing resource cases:

- Unknown routes should return `404 Not Found`.
- Valid product routes with missing product IDs should return `404 Not Found`.
- The response body should clearly explain that the product was not found.

Bad input cases:

- Invalid path parameters, such as a non-integer product ID, should return
  `422 Unprocessable Entity`.
- Invalid request bodies, such as missing required fields, empty names, or bad
  prices, should return `422 Unprocessable Entity`.
- Duplicate SKUs should return a deliberate application error, likely
  `409 Conflict`.

FastAPI and Starlette exception types to understand:

- `HTTPException`: raise this from route or service code for deliberate
  application errors, such as missing products or duplicate SKUs.
- `StarletteHTTPException`: Starlette's lower-level HTTP exception type,
  commonly involved in framework-generated errors such as unknown routes.
- `RequestValidationError`: FastAPI's validation error for invalid path,
  query, or body inputs.

Do not customize exception handlers immediately. First learn FastAPI's default
responses, then customize only if the default shape is not useful for the API
contract.

# TODO
Rewatch part 5 later since it has logic on how to add users to a table and associated endpoints
Watch BEFORE authentication part

Part of models.py snippet
```python
# TODO: Later migrate this to Auth service
# TODO: Integrate passwords
class User(Base):
    __tablename__ = "users"

    id = Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
```

## Databases
When migrating from SQLite to Postgres, 
migrate from multiple DBs to a single shared DB with different tables per service.

## Bulk Endpoints
Consider later "bulk" endpoints for creating, updating, getting, or deleting more than one object at once.

# Initial Feature Branches

Get all services to meet these requirements:
- [ ] CRUD Functionality
- [ ] Uses Pydantic Schemas
- [ ] Integrated with a SQLite database using SQLAlchemy

Services:
[ ] Inventory Service
[ ] Ordering Service
[ ] Auth Service
[ ] Search Service
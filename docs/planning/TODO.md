# TODO

Later edit python functions to support asynchronous calls

## Product Service Initial Plan
The branch should support:

  - Creating products.
  - Listing products.
  - Fetching products by ID or SKU.
  - Updating products and prices.
  - Deactivating products.
  - Persisting products in PostgreSQL.
  - Validating requests with Pydantic.
  - Automated tests.
  - Running through Docker Compose.

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

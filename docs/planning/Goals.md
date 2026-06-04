# Project Goals

## Purpose

This is a learning project for gaining practical experience after covering
Docker basics. The project is a small mock e-commerce system built from
containerized FastAPI microservices and deployed with Docker Swarm.

The purpose is not to build a production-ready store. The purpose is to
practice designing, building, connecting, and operating a complete
multi-service application.

## Primary Outcome

Complete one end-to-end customer journey:

1. A user can register and log in.
2. The user can find a product.
3. The user can place an order at the product's current price.
4. Inventory is reserved when the order is accepted.
5. The user can cancel the order and release the reserved inventory.

The project is successful when this journey works across independently
containerized services running in Docker Swarm.

## Learning Priorities

In priority order, I want to learn:

1. **Microservice design**
   - Define clear service responsibilities and API contracts.
   - Keep data ownership within the service that owns the domain.
   - Handle communication and failures between services.
2. **Containers and local development**
   - Build useful, repeatable Docker images.
   - Run the complete system with Docker Compose.
   - Use Docker Bake to build multiple service images.
3. **Container orchestration**
   - Deploy and operate the system with Docker Swarm.
   - Practice service discovery, configuration, secrets, scaling, and updates.
4. **Data persistence**
   - Use PostgreSQL with separate data ownership for each stateful service.
   - Manage schema changes and persistent container data.
5. **Supporting capabilities**
   - Implement JWT-based authentication.
   - Add product search after the core ordering flow works.

## Planned Service Boundaries

| Service | Owns | Does not own |
| --- | --- | --- |
| Product Service | Product identity, catalog metadata, and current pricing | Stock levels and orders |
| Inventory Service | Available stock and stock reservations | Product metadata and prices |
| Ordering Service | Orders, order state, and coordination of order placement | Product prices and stock levels |
| Auth Service | User registration, login, and token validation | Commerce data |
| Search Service | Product discovery and its search index | Authoritative product data |

Pricing starts inside the Product Service. It should only become a separate
service after the initial system works and there is a concrete learning reason
to split it.

## Build Plan

Each phase should produce a working, testable increment. Do not start the next
phase until the current phase's exit criteria are met.

### Phase 1: Product Service

Build the stable catalog contract needed by the other services.

Exit criteria:

- Products and current prices are stored in PostgreSQL.
- Products can be created, updated, listed, and fetched by ID or SKU.
- The service has automated tests for its main behavior.
- The service runs in a container through Docker Compose.
- Its API contract and ownership boundaries are documented.

### Phase 2: Inventory Service

Add stock tracking and reservation using product IDs.

Exit criteria:

- Stock can be added and queried.
- Stock can be reserved and released without allowing negative availability.
- The service owns its own PostgreSQL data.
- Product and Inventory services run together through Docker Compose.

### Phase 3: Ordering Service

Complete the core unauthenticated commerce workflow.

Exit criteria:

- An order fetches the current price from Product Service.
- An order reserves stock through Inventory Service.
- Failed reservations reject the order cleanly.
- Cancelling an order releases its stock reservation.
- The complete product-to-order workflow has an automated integration test.

### Phase 4: Auth Service

Add users and protect the ordering workflow.

Exit criteria:

- A user can register and log in.
- The service issues and validates JWTs.
- Ordering requires a valid user token.
- Auth data remains independent from commerce data.

### Phase 5: Search Service

Add product discovery without changing ownership of catalog data.

Exit criteria:

- Products can be searched using a deliberately chosen search technology.
- Product Service remains the authoritative source of product data.
- Index synchronization behavior and limitations are documented.

### Phase 6: Orchestration and Operations

Deploy and operate the completed workflow in Docker Swarm.

Exit criteria:

- Docker Bake builds all service images.
- Docker Swarm deploys the complete application.
- Configuration and secrets are kept out of images and source code.
- Persistent data survives service restarts.
- At least one service can be scaled and updated without breaking the workflow.

## Scope Guardrails

Until the primary outcome works in Docker Swarm:

- Do not build a production-ready frontend; API clients or a minimal UI are
  enough.
- Do not add payment processing, shipping, promotions, recommendations, or
  other store features.
- Do not split pricing out of Product Service.
- Do not replace JWT auth with a third-party provider.
- Do not introduce asynchronous messaging unless a current workflow clearly
  needs it.
- Do not optimize for high scale or production-grade availability.
- Prefer the simplest implementation that teaches the goal of the current
  phase.

Ideas outside this scope should go into `TODO.md` rather than interrupting the
current phase.

## Git Workflow

### Commit Style

Commit messages follow the modified Conventional Commits style defined in
[`commit-message-rules.md`](../../commit-message-rules.md):

```text
<type>[(optional scope)][!]: <description>
```

Each commit should contain one logical change. Use a service name as the scope
when a change belongs to one service, and leave the scope out for
repository-wide changes.

Examples:

```text
feat(product): add product lookup endpoint
test(inventory): add stock reservation tests
build: add root Docker Compose file
```

Commit descriptions should be concise, use the imperative mood, and explain
what the commit does. Use a body when the reason, tradeoffs, or important
implementation details are not clear from the description alone.

### Branching Strategy

- `main` represents stable, completed project milestones.
- `dev` is the integration branch for active development.
- Start the initial build of each service from `dev` on a short-lived
  `feature/<service>` branch, such as `feature/product` or
  `feature/inventory`.
- Keep each feature branch focused on its service's current phase and merge it
  back into `dev` when that phase's exit criteria are met.
- Merge `dev` into `main` when the integrated system reaches a stable,
  documented milestone.
- Delete feature branches after they are merged.

For later unforeseen changes, create another short-lived branch from `dev`
named for the kind of change and affected area, such as
`fix/inventory-reservation` or `refactor/product-pricing`. Merge it back into
`dev` after the change is tested. The exact workflow can evolve when repeated
needs reveal a reason to change it.

## Working Rules

- Work on one phase at a time.
- Keep the system runnable at the end of each phase.
- Add tests for important behavior and cross-service workflows.
- Document decisions that affect service boundaries or communication.
- Treat failures between services as expected behavior, not exceptional edge
  cases.
- Review this document before expanding scope or adopting a new technology.

When choosing the next task, ask:

1. Is it required to meet the current phase's exit criteria?
2. Does it directly support one of the learning priorities?
3. Is it the smallest useful step toward a working increment?

If the answer to the first two questions is no, record the idea in `TODO.md`
and return to the current phase.

## Current Focus

**Phase 1: Product Service**

The next milestone is a containerized Product Service backed by PostgreSQL,
with a documented API contract and automated tests.

## Definition of Project Complete

This learning project is complete when:

- The primary customer journey works end to end.
- Every service runs in its own container and owns its own data.
- Docker Compose supports local development.
- Docker Bake builds the service images.
- Docker Swarm deploys and operates the complete system.
- The repository explains the architecture, key decisions, and how to run it.

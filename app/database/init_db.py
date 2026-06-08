# These imports are for foreign keys
from app.database.database import Base, engine
from app.inventory_service import models as inventory_models
from app.product_catalog import models as product_models


# Create Tables if they do not already exist
# Idempotent so can be run multiple times
def init_db() -> None:
    Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Database URL
# Everything after /// is current url
# (Our case is current directory product.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/database/database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Enables Multithreading
    connect_args={"check_same_thread": False},
)

# Creates database session
# Flags enable us more control when
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Provides session to our routes via Dependency Injection
def get_db():
    with SessionLocal() as db:
        yield db

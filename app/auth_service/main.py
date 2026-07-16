from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_service import models
from app.auth_service.models import User
from app.auth_service.schemas import UserCreate, UserResponse, UserUpdate
from app.database.database import get_db
from app.database.init_db import init_db

init_db()
app = FastAPI()
password_hasher = PasswordHash.recommended()


# Hashes Password based on Argon2 Algorithm
def compute_password_hash(password: str) -> str:
    return password_hasher.hash(password)


# Creates a new user
@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> User:

    result = db.execute(select(models.User).where(User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )

    new_user = models.User(
        # Hash password before
        email=user.email,
        username=user.username,
        password_hash=compute_password_hash(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Gets a list of all current users
@app.get(
    "/api/users/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
) -> list[UserResponse]:

    result = db.execute(select(models.User))

    return list(result.scalars().all())


# Gets a specific user
@app.get(
    "/api/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> User:

    result = db.execute(select(models.User).where(User.id == user_id))

    stored_user = result.scalars().first()

    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return stored_user


# Partially updates a specific user
@app.patch(
    "/api/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_partial(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    result = db.execute(select(models.User).where(models.User.id == user_id))

    stored_user = result.scalars().first()

    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    update_data = user_data.model_dump(exclude_unset=True)

    password = update_data.pop("password", None)

    if password is not None:
        update_data["password_hash"] = compute_password_hash(password)

    for field, value in update_data.items():
        setattr(stored_user, field, value)

    db.commit()
    db.refresh(stored_user)
    return stored_user


# Deletes a specific user
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    result = db.execute(select(models.User).where(User.id == user_id))

    stored_user = result.scalars().first()

    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(stored_user)
    db.commit()


## Need login later

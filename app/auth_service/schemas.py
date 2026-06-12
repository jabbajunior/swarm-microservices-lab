from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(min_length=1, max_length=64)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=32)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=64)
    email: EmailStr | None = Field(default=None, min_length=1, max_length=64)
    password: str | None = Field(default=None, min_length=8, max_length=32)

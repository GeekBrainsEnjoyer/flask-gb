from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserIn(BaseModel):
    first_name: str = Field(max_length=32)
    second_name: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str


class User(UserIn):
    id: int

    class Config:
        orm_mode = True


class ItemIn(BaseModel):
    name: str
    description: str = None
    price: int


class Item(ItemIn):
    id: int

    class Config:
        orm_mode = True


class OrderIn(BaseModel):
    user_id: int
    item_id: int
    created_at: datetime = Field(default=datetime.now())
    is_delivered: bool = Field(default=False)


class Order(OrderIn):
    id: int

    class Config:
        orm_mode = True

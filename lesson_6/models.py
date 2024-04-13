from typing import Optional
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(__name_pos=String(32))
    second_name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(128))
    password: Mapped[str]

    def __repr__(self) -> str:
        return self.first_name


class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]

    def __repr__(self) -> str:
        return self.name


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    created_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    is_delivered: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.created_at}"

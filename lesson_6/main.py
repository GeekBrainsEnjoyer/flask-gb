import databases
from typing import List
import sqlalchemy
from fastapi import FastAPI

from models import Base
from schemas import ItemIn, OrderIn, User, Item, Order, UserIn

DATABASE_URL = 'sqlite:///mydatabase.db'
engine = sqlalchemy.create_engine(DATABASE_URL, echo=True,
                                  connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

users = Base.metadata.tables['users']
items = Base.metadata.tables['items']
orders = Base.metadata.tables['orders']

database = databases.Database(DATABASE_URL)

app = FastAPI()


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(first_name=user.first_name,
                                  second_name=user.second_name, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id ==
                                 user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.get("/items/", response_model=List[Item])
async def read_items():
    query = items.select()
    return await database.fetch_all(query)


@app.post("/items/", response_model=Item)
async def create_item(item: ItemIn):
    query = items.insert().values(name=item.name,
                                  description=item.description, price=item.price)
    last_record_id = await database.execute(query)
    return {**item.model_dump(), "id": last_record_id}


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, new_item: ItemIn):
    query = items.update().where(items.c.id ==
                                 item_id).values(**new_item.model_dump())
    await database.execute(query)
    return {**new_item.model_dump(), "id": item_id}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'Item deleted'}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id,
                                   item_id=order.item_id, is_delivered=order.is_delivered, created_at=order.created_at)
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id ==
                                  order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}

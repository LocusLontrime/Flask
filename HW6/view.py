from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from HW6 import models

app = FastAPI()
DATABASE_URL = 'sqlite:///homework_6.db'

db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users', metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('name', sqlalchemy.String(32)),
                         sqlalchemy.Column('surname', sqlalchemy.String(32)),
                         sqlalchemy.Column('email', sqlalchemy.String(32)),
                         sqlalchemy.Column('password', sqlalchemy.String(32)))

products = sqlalchemy.Table('products', metadata,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('name', sqlalchemy.String(32)),
                            sqlalchemy.Column('description', sqlalchemy.String(128)),
                            sqlalchemy.Column('price', sqlalchemy.Float))

orders = sqlalchemy.Table('orders', metadata,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column('products_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column('date_', sqlalchemy.DateTime),
                          sqlalchemy.Column('status', sqlalchemy.String(32)))

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


# Users
@app.get('/users/', response_model=List[models.UserModel])
async def get_user():
    query = users.select()
    return await db.fetch_all(query)


@app.get('/users/{user_id}', response_model=models.UserModel)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


@app.post('/users/', response_model=models.UserModel)
async def set_user(user: models.User):
    query = users.insert().values(**user.dict())
    new_id = await db.execute(query)
    return {**user.dict(), 'id': new_id}


@app.put('/users/{user_id}', response_model=models.UserModel)
async def update_user(user_id: int, user: models.User):
    query = users.update().where(users.c.id == user_id).values(**user.dict())
    await db.execute(query)
    return {**user.dict(), "id": user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}


# Orders:
@app.get('/orders/', response_model=List[models.OrderModel])
async def get_order():
    query = orders.select()
    return await db.fetch_all(query)


@app.get('/orders/{order_id}', response_model=models.OrderModel)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await db.fetch_one(query)
    return order


@app.post('/orders/{user_id}/{product_id}', response_model=models.OrderModel)
async def set_order(order: models.Order, user_id: int, product_id: int):
    user = await db.fetch_one(users.select().where(users.c.id == user_id))
    if user:
        product = await db.fetch_one(products.select().where(products.c.id == product_id))
        if product:
            query = orders.insert().values(date_=order.date_, status=order.status, user_id=user_id,
                                           products_id=product_id)
            new_id = await db.execute(query)
            return {**order.dict(), 'id': new_id}
        return HTTPException(status_code=404, detail="This product is not found!")
    return HTTPException(status_code=404, detail="To place an order, you need to log in")


@app.put('/orders/{order_id}', response_model=models.OrderModel)
async def update_order(order: models.Order, order_id: int):
    query = orders.update().where(orders.c.id == order_id).values(date_=order.date_, status=order.status)
    await db.execute(query)
    return {**order.dict(), 'id': order_id}


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {'message': 'Order deleted'}


# Products
@app.get('/products', response_model=List[models.ProductModel])
async def get_products():
    query = products.select()
    return await db.fetch_all(query)


@app.get('/products/{product_id}', response_model=models.ProductModel)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await db.fetch_one(query)


@app.post('/products/', response_model=models.ProductModel)
async def set_product(product: models.Product):
    query = products.insert().values(**product.dict())
    product_id = await db.execute(query)
    return {**product.dict(), 'id': product_id}


@app.put('/products/{product_id}', response_model=models.ProductModel)
async def update_product(product_id: int, product: models.Product):
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await db.execute(query)
    return {**product.dict(), 'id': product_id}


@app.delete('/products/{product_id}')
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {'message': 'Product deleted'}
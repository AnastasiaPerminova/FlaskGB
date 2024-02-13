# Задание №6
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление

from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, insert, update

from database import startup, shutdown, db
from schemas import UserInSchema, UserSchema, ProductInSchema, ProductSchema, OrderInSchema, OrderSchema, Status
from models import UserModel, ProductModel, OrderModel
from tools import get_password_hash
from passlib.context import CryptContext

app = FastAPI(title='Seminar_6_Homework')
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.user_id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.dict()  # .model_dump()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'user_id': user_id}


@app.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.user_id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.dict(exclude_unset=True)
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.user_id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.user_id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = select(UserModel).where(UserModel.user_id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.user_id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь с id={db_user.user_id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.get("/products/", response_model=List[ProductSchema])
async def get_all_products() -> List[ProductSchema]:
    """Получение списка всех товаров: GET /products/"""
    query = select(ProductModel)
    products = await db.fetch_all(query)
    if products:
        return products
    raise HTTPException(status_code=404, detail="Нет ни одного товара")


@app.get('/products/{product_id}', response_model=ProductSchema)
async def get_single_product(product_id: int) -> ProductSchema:
    """Получение информации о конкретном товаре: GET /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.product_id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.post('/products/', response_model=ProductSchema)
async def create_product(product: ProductInSchema) -> dict:
    """Создание нового товара: POST /products/"""
    product_dict = product.dict()  # .model_dump()

    query = insert(ProductModel).values(**product_dict)
    product_id = await db.execute(query, product_dict)
    return {**product_dict, 'product_id': product_id}


@app.put('/products/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product: ProductInSchema) -> ProductSchema:
    """Обновление информации о товаре: PUT /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.product_id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        updated_product = product.dict(exclude_unset=True)
        query = update(ProductModel).where(ProductModel.product_id == product_id).values(updated_product)
        await db.execute(query)
        return await db.fetch_one(select(ProductModel).where(ProductModel.product_id == product_id))
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.delete("/products/{product_id}")
async def delete_product(product_id: int) -> dict:
    """Удаление товара: DELETE /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.product_id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        query = delete(ProductModel).where(ProductModel.product_id == product_id)
        await db.execute(query)
        return {'detail': f'Товар с id={db_product.product_id} удален'}
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.get("/orders/", response_model=List[OrderSchema])
async def get_all_orders() -> List[OrderSchema]:
    """Получение списка всех заказов: GET /orders/"""
    query = select(OrderModel)
    orders = await db.fetch_all(query)
    if orders:
        return orders
    raise HTTPException(status_code=404, detail="Нет ни одного заказа")


@app.get('/orders/{order_id}', response_model=OrderSchema)
async def get_single_order(order_id: int) -> OrderSchema:
    """Получение информации о конкретном заказе: GET /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.order_id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app.post('/orders/', response_model=OrderSchema)
async def create_order(order: OrderInSchema) -> dict:
    """Создание нового заказа: POST /orders/"""
    order_dict = order.dict()  # .model_dump()

    query = insert(OrderModel).values(**order_dict)
    order_id = await db.execute(query, order_dict)
    return {**order_dict, 'order_id': order_id}


@app.put('/orders/{order_id}', response_model=OrderSchema)
async def update_order(order_id: int, order: OrderInSchema) -> ProductSchema:
    """Обновление информации о заказе: PUT /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.order_id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        updated_order = order.dict(exclude_unset=True)
        query = update(OrderModel).where(OrderModel.order_id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(OrderModel).where(OrderModel.order_id == order_id))
    raise HTTPException(status_code=404, detail="Заказ не найден")


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int) -> dict:
    """Удаление заказа: DELETE /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.order_id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        query = delete(OrderModel).where(OrderModel.order_id == order_id)
        await db.execute(query)
        return {'detail': f'Заказ с id={db_order.order_id} удален'}
    raise HTTPException(status_code=404, detail="Заказ не найден")
from datetime import datetime

from uvicorn import run as run_app
from fastapi import FastAPI


from database import startup, shutdown, db
from sqlalchemy import select, delete, insert, update

from models import UserModel, ProductModel, OrderModel
from schemas import Status
from tools import pwd_context
from app import app

app1 = FastAPI()
app1.mount("/homework", app)


@app1.get("/")
async def read_item():
    return {"message": "Seminar_6. Homework"}

if __name__ == '__main__':
    import asyncio

    asyncio.run(startup())


    async def clear_users_db():
        query = delete(UserModel)
        await db.execute(query)
        query = insert(UserModel)

        for i in range(11):
            password = pwd_context.hash(f'password{i}')
            new_user = {"user_name": f"name{i}",
                        "user_surname": f"user{i}", "email": f"user{i}@mail.ru", "password": f"{password}"}
            await db.execute(query, new_user)


    asyncio.run(clear_users_db())

    async def clear_products_db():
        query = delete(ProductModel)
        await db.execute(query)
        query = insert(ProductModel)
        price = 100
        for i in range(21):
            new_product = {"product_name": f"name{i}", "product_description": f"description{i}", "price": price + i}
            await db.execute(query, new_product)


    asyncio.run(clear_products_db())


    async def clear_orders_db():
        query = delete(OrderModel)
        await db.execute(query)
        query = insert(OrderModel)

        for i in range(11):
            if i % 2 == 0:
                status = Status.DONE
            else:
                status = Status.IN_PROGRESS
            for j in range(21):
                date = f'2024-01-{i+1}'
                order_date = datetime.strptime(date, '%Y-%m-%d').date()
                new_order = {"user_id": i, "product_id": j, "order_date": order_date, "status": status}
                await db.execute(query, new_order)

    asyncio.run(clear_orders_db())

    run_app("main:app1", host='127.0.0.1', port=8000, reload=True)

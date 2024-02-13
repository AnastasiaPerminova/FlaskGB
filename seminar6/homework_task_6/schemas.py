# Задание №6
# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).

import datetime
from enum import Enum
from pydantic import EmailStr, BaseModel, Field


class Status(Enum):
    """Перечисление статусов заказов"""
    DONE = 'Выполнен'
    IN_PROGRESS = 'Выполняется'


class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    user_name: str = Field(..., max_length=25, min_length=3,
                           title='Задается user_name пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    user_surname: str = Field(..., max_length=35, min_length=3,
                              title='Задается user_surname пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr = Field(..., title='Задается email пользователя')

    password: str = Field(..., title='Задается пароль пользователя')


class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    user_id: int


class ProductInSchema(BaseModel):
    """Модель товара без id"""
    product_name: str = Field(..., max_length=25, min_length=3,
                              title='Задается product_name пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    product_description: str = Field(default=None, max_length=1000, title='Задается description товара')
    price: float = Field(..., title='Задается цена товара')


class ProductSchema(ProductInSchema):
    """Модель товара с id"""
    product_id: int


class OrderInSchema(BaseModel):
    """Модель заказа без id"""
    user_id: int
    product_id: int
    order_date: datetime.date = Field(..., title='Задается дата заказа"')
    status: Status = Status.IN_PROGRESS


class OrderSchema(OrderInSchema):
    """Модель заказа с id"""
    order_id: int

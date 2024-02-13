# Задание №6
# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.
#

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from schemas import Status
Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'users_task_6'
    user_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_name = Column(String(length=50), unique=True, index=True)
    user_surname = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.user_name

    def __repr__(self):
        return f'User(id={self.user_id}, user_name={self.user_name}, user_surname={self.user_surname} email={self.email})'


class ProductModel(Base):
    """Таблица Products"""
    __tablename__ = 'products_task_6'
    product_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_name = Column(String(length=50), unique=True, index=True)
    product_description = Column(String(length=1000), index=True)
    price = Column(Float, index=True)

    def __str__(self):
        return f'{self.product_name} - price: {self.price}'

    def __repr__(self):
        return f'Product(id={self.product_id}, product_name={self.product_name},' \
               f' product_description={self.product_description}, price={self.price})'


class OrderModel(Base):
    """Таблица Orders"""
    __tablename__ = 'orders_task_6'
    order_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(UserModel.user_id))
    product_id = Column(Integer, ForeignKey(ProductModel.product_id))
    order_date = Column(Date)
    status = Column(Enum(Status), nullable=False)

    def __str__(self):
        return f'{self.order_id} - status: {self.status}'

    def __repr__(self):
        return f'Order(id={self.order_id}, user_id={self.user_id},' \
               f' product_id={self.product_id}, order_date={self.order_date}, status={self.status})'


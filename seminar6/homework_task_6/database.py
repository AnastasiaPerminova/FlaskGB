import sqlalchemy
import databases
from sqlalchemy.pool import StaticPool
from models import UserModel, ProductModel, OrderModel

DATABASE_URL = "sqlite:///homework_task_6.db"
db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def startup():
    await db.connect()
    engine = sqlalchemy.create_engine(DATABASE_URL, echo=True, poolclass=StaticPool,
                                      connect_args={"check_same_thread": False})
    UserModel.metadata.create_all(engine)
    ProductModel.metadata.create_all(engine)
    OrderModel.metadata.create_all(engine)


async def shutdown():
    await db.disconnect()


async def get_db_session():
    async with db.transaction():
        yield

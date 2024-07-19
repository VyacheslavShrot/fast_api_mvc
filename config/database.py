from databases import Database
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

# Read ENV File
env = Env()
env.read_env('.env')

MYSQL_DATABASE = env("MYSQL_DATABASE")
MYSQL_USER = env("MYSQL_USER")
MYSQL_PASSWORD = env("MYSQL_PASSWORD")

DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/{MYSQL_DATABASE}"

database: Database = Database(DATABASE_URL)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "auth_plugin": "mysql_native_password"
    }
)

async_session: sessionmaker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

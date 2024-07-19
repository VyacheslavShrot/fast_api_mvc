from fastapi import FastAPI
from sqlalchemy.future import select

from config.database import database, async_session
from config.models import users

# Create Web APP FastAPI
app: FastAPI = FastAPI(
    title="Fast API MVC"
)


@app.on_event("startup")
async def startup():
    """
    Connect To DataBase
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Disconnect To DataBase
    """
    await database.disconnect()


@app.get("/app-status")
async def app_status():
    """
    Just APP Status
    """
    return {
        "status": "success"
    }


@app.get("/db/status/users", response_model=list[dict])
async def db_status_users():
    """
    Just for DB Status of Checking Successful Created Database and Users Table
    """
    async with async_session() as session:
        query = select(users)
        result = await session.execute(query)
        return result.scalars().all()

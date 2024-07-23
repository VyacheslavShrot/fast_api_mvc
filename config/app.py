from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import Select, Result
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from apis.user_apis import users_router
from config.database import database, async_session
from config.models import User

# Create Web APP FastAPI
app: FastAPI = FastAPI(
    title="Fast API MVC"
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(
        request: Request,
        exc: HTTPException
) -> JSONResponse:
    """
    Custom HTTPException Response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail
        }
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
        # Get Users
        query: Select = select(User)

        # Execute Query
        result: Result = await session.execute(query)
        return result.scalars().all()


# Register Routers
app.include_router(users_router)

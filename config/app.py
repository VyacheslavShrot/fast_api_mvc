from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import text, CursorResult
from starlette.responses import JSONResponse

from apis.user_apis import users_router
from config.database import database, async_session

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


@app.get("/db-status")
async def db_status():
    """
    Just for DB Status of Checking Successful Working with DB
    """
    async with async_session() as session:
        # Perform a Simple Query to Check Database Connection
        result: CursorResult = await session.execute(text("SELECT 1"))
        return JSONResponse(
            {
                "result": result.scalar()
            },
            status_code=200
        )


# Register Routers
app.include_router(users_router)

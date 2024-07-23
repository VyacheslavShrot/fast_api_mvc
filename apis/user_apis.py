import bcrypt
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import Select, Result, Row
from sqlalchemy.future import select

from apis.utils.token import create_access_token
from config.database import async_session
from config.logger import logger
from config.models import User
from config.schemas import SignUp

# Register APIs
users_router: APIRouter = APIRouter()


@users_router.post("/user/signup")
async def signup(
        body: SignUp
) -> JSONResponse:
    """
    SignUp API for Creating User and JWT Access Token
    """
    try:
        async with async_session() as session:
            # Get User with Input Email
            query: Select = select(User).filter_by(email=body.email)

            # Execute Query
            result: Result = await session.execute(query)

            existing_user: Row = result.scalars().first()
            if existing_user:
                return JSONResponse(
                    {
                        "error": "Such User with Such Email Already Exist"
                    },
                    status_code=400
                )

            # Create Hash of Password
            hashed_password: bytes = bcrypt.hashpw(
                body.password.encode('utf-8'),
                bcrypt.gensalt()
            )

            # Create User
            user: User = User(
                email=body.email, password=hashed_password
            )

            # Add User into Session for Saving
            session.add(user)

            # Save User into DB
            await session.commit()

            # Generate JWT Token
            token: str = create_access_token(
                {
                    "user_email": user.email
                }
            )

            return JSONResponse(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "email": user.email
                    },
                    "token": token
                },
                status_code=201
            )
    except Exception as e:
        logger.error(f"An error occurred while signup user | {e}")
        return JSONResponse(
            {
                "error": f"An error occurred while signup user | {e}"
            },
            status_code=500
        )

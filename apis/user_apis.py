import bcrypt
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import Select, Result, Row
from sqlalchemy.future import select

from apis.utils.token import create_access_token
from config.database import async_session
from config.logger import logger
from config.models import User
from config.schemas import SignUpOrLogin

# Register APIs
users_router: APIRouter = APIRouter()


@users_router.post("/user/signup")
async def signup(
        body: SignUpOrLogin
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

            existing_user: User = result.scalars().first()
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


@users_router.post("/user/login")
async def login(
        body: SignUpOrLogin
) -> JSONResponse:
    """
    Login API for Check Input Email and Password and Return JWT Access Token
    """
    try:
        async with async_session() as session:
            # Get User with Input Email
            query: Select = select(User).filter_by(email=body.email)

            # Execute Query
            result: Result = await session.execute(query)

            existing_user: User = result.scalars().first()
            if not existing_user:
                return JSONResponse(
                    {
                        "error": "Such User with Such Email Are Not Exist"
                    },
                    status_code=400
                )

            # Check Password
            validated_password: bool = bcrypt.checkpw(
                password=body.password.encode('utf-8'),
                hashed_password=existing_user.password.encode('utf-8')
            )
            if not validated_password:
                return JSONResponse(
                    {
                        "error": "Invalid Password"
                    },
                    status_code=400
                )

            # Generate JWT Token
            token: str = create_access_token(
                {
                    "user_email": existing_user.email
                }
            )

            return JSONResponse(
                {
                    "success": True,
                    "user": {
                        "id": existing_user.id,
                        "email": existing_user.email
                    },
                    "token": token
                },
                status_code=200
            )
    except Exception as e:
        logger.error(f"An error occurred while login user | {e}")
        return JSONResponse(
            {
                "error": f"An error occurred while login user | {e}"
            },
            status_code=500
        )

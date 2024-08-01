from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi import Header
from sqlalchemy import Select, Result
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, sessionmaker

from config.database import env
from config.models import User

# JWT Conf
SECRET_KEY = env("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: str = env("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(
        data: dict,
        expires_delta: timedelta = None
) -> str:
    """
    Create JWT Access Token
    """
    # Copy Data
    to_encode: dict = data.copy()

    if not to_encode.get("user_email", None):
        raise ValueError(
            "Data must contain 'user_email' to identification user in future"
        )

    # Create Expire Date of Token
    if expires_delta:
        expire: datetime = datetime.utcnow() + expires_delta
    else:
        expire: datetime = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    # Save Expire Date into Data
    to_encode.update(
        {
            "exp": expire,
            "user_email": to_encode["user_email"]
        }
    )

    # Create Access Token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(
        token: str
) -> dict | bool:
    """
    Decode JWT Access Token
    """
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.PyJWTError:
        return False


def get_token_from_header(
        authorization: str = Header(None)
) -> str | bool:
    """
    Get Token from Header like Bearer
    """
    if not authorization or not authorization.startswith("Bearer "):
        return False
    return authorization.split(" ")[1]


def get_current_user_email(
        token: str | bool = Depends(get_token_from_header)
) -> str | bool:
    """
    Get Current User Email by JWT Token
    """
    if not token:
        return False

    # Decode Token
    decoded_token: dict | bool = decode_access_token(token)
    if not decoded_token:
        return False

    # Get User Email from Token
    user_email: str = decoded_token["user_email"]

    return user_email


async def get_current_user(
        session,
        current_user_email: str
) -> User:
    """
    Get Current User Object with Database Async Session and PreLoad User Posts
    """

    # Get User with Email from Token
    query: Select = select(User).filter_by(email=current_user_email).options(selectinload(User.posts))

    # Execute Query
    result: Result = await session.execute(query)

    user: User = result.scalars().first()

    return user

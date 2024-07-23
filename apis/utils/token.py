from datetime import datetime, timedelta

import jwt

from config.database import env

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
) -> dict:
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
        raise ValueError("Invalid Token")

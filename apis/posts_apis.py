from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Select, Result, Row
from sqlalchemy.future import select

from apis.utils.token import get_current_user_email
from config.database import async_session
from config.logger import logger
from config.models import User, Post
from config.schemas import PostAdd

# Register APIs
posts_router: APIRouter = APIRouter()


@posts_router.post("/post/add")
async def add_post(
        body: PostAdd,
        current_user_email: str | bool = Depends(get_current_user_email)
) -> JSONResponse:
    """
    Add Post API with Auth Token Requireid for Creating Post
    """
    try:
        async with async_session() as session:
            if not current_user_email:
                return JSONResponse(
                    {
                        "error": "invalid Token"
                    },
                    status_code=401
                )

            # Get User with Email from Token
            query: Select = select(User).filter_by(email=current_user_email)

            # Execute Query
            result: Result = await session.execute(query)

            user: User = result.scalars().first()

            # Create Post
            post: Post = Post(
                user_id=user.id,
                text=body.text
            )

            # Add Post into Session for Saving
            session.add(post)

            # Save User into DB
            await session.commit()

            return JSONResponse(
                {
                    "success": True,
                    "post": {
                        "id": post.id,
                        "user_email": post.user.email,
                        "text": post.text
                    }
                },
                status_code=201
            )
    except Exception as e:
        logger.error(f"An error occurred while add post | {e}")
        return JSONResponse(
            {
                "error": f"An error occurred while add post | {e}"
            },
            status_code=500
        )

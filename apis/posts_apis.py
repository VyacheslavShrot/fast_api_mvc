from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Select, Result
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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
            if not user:
                return JSONResponse(
                    {
                        "error": "Don't Exist Such User with Such Email"
                    },
                    status_code=401
                )

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


@posts_router.get("/posts")
async def get_posts(
        current_user_email: str | bool = Depends(get_current_user_email)
) -> JSONResponse:
    """
    Get ALL User Posts API with Auth Token Requireid and Caching Response
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
            query: Select = select(User).filter_by(email=current_user_email).options(selectinload(User.posts))

            # Execute Query
            result: Result = await session.execute(query)

            user: User = result.scalars().first()
            if not user:
                return JSONResponse(
                    {
                        "error": "Don't Exist Such User with Such Email"
                    },
                    status_code=401
                )

            return JSONResponse(
                {
                    "success": True,
                    "posts": [
                        {
                            "id": post.id,
                            "user_email": post.user.email,
                            "text": post.text
                        }
                        for post in user.posts
                    ]
                },
                status_code=200
            )
    except Exception as e:
        logger.error(f"An error occurred while get posts | {e}")
        return JSONResponse(
            {
                "error": f"An error occurred while get posts | {e}"
            },
            status_code=500
        )

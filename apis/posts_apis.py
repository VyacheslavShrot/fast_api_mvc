from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Select, Result
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from apis.utils.cache import get_and_add_user_posts_into_cache, delete_post_from_cache
from apis.utils.token import get_current_user_email
from config.database import async_session
from config.logger import logger
from config.models import User, Post
from config.schemas import PostAdd, PostDelete

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

            # If Cache is Exist -> Add New Post into Cache Posts List
            await get_and_add_user_posts_into_cache(
                post=post,
                user_email=current_user_email
            )

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

            # Get Cached Posts
            cached_posts: list[dict] | None = await get_and_add_user_posts_into_cache(
                user_email=current_user_email
            )
            if not cached_posts:
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

                # Get ALL User Posts
                user_posts: list[Post] = user.posts

                # Format Response
                posts: list[dict] = [
                    {
                        "id": post.id,
                        "user_email": post.user.email,
                        "text": post.text
                    }
                    for post in user_posts
                ]

                # Add User Posts into Cache
                await get_and_add_user_posts_into_cache(
                    post=posts,
                    user_email=current_user_email
                )

            return JSONResponse(
                {
                    "success": True,
                    "posts": cached_posts if cached_posts else posts
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


@posts_router.post("/post/delete")
async def delete_post(
        body: PostDelete,
        current_user_email: str | bool = Depends(get_current_user_email)
) -> JSONResponse:
    """
    Delete Post API with Auth Token Requireid for Deleting Post
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

            # Get Post by Input Post Id
            query: Select = select(Post).filter_by(id=body.post_id)

            # Execute Query
            result: Result = await session.execute(query)

            post: Post = result.scalars().first()
            if not post:
                return JSONResponse(
                    {
                        "error": "Don't Exist Such Post with Such Post Id"
                    },
                    status_code=400
                )

            # Get ALL user Posts
            user_posts: list[Post] = user.posts
            if not user_posts:
                return JSONResponse(
                    {
                        "error": "Don't Exist Such Post for Such User"
                    },
                    status_code=400
                )

            # Create List of ALL User Posts Ids
            user_posts_id: list = [user_post.id for user_post in user_posts]

            # Check if That Post is About This User
            if post.id not in user_posts_id:
                return JSONResponse(
                    {
                        "error": "That Post is Not About This User"
                    },
                    status_code=400
                )

            # Add Post into Session for Deleting
            await session.delete(post)

            # Delete Post from DB
            await session.commit()

            # Update Cached Posts Without Deleted Post
            await delete_post_from_cache(
                user_email=current_user_email,
                post_id=post.id
            )

            return JSONResponse(
                {
                    "success": True
                },
                status_code=200
            )
    except Exception as e:
        logger.error(f"An error occurred while delete post | {e}")
        return JSONResponse(
            {
                "error": f"An error occurred while delete post | {e}"
            },
            status_code=500
        )

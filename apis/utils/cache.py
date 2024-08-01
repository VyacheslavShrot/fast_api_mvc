from aiocache import caches

from config.models import Post

# Cache Config
caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'ttl': 300  # 5 Minutes
    }
})

cache = caches.get('default')


async def get_cached_posts_and_cache_key(
        user_email: str
) -> tuple[
    list | None,
    str
]:
    """
    Get Cached Posts And Cache Key by User Email
    """
    # Cache Key for Posts
    cache_key: str = f"{user_email}_posts"

    # Get Cached Posts
    cached_posts: list | None = await cache.get(cache_key, None)

    return cached_posts, cache_key


async def get_and_add_user_posts_into_cache(
        user_email: str,
        post: Post | list = None
) -> list[dict] | None:
    """
    Get From Cache And Add Posts Into Cache
    """

    # Get Cached Posts and Cache Key
    cached_posts, cache_key = await get_cached_posts_and_cache_key(
        user_email=user_email
    )
    cached_posts: list | None
    cache_key: str

    # If Post Object Exist
    if post:

        # If One Post Object -> Than Mean Called This Function from "Add Post API"
        if isinstance(post, Post):

            # If Exist Cached Posts List -> Append Into This List New Post
            if cached_posts:
                cached_posts.append(
                    {
                        "id": post.id,
                        "user_email": post.user.email,
                        "text": post.text
                    }
                )

        # If Post = List Object -> Than Mean Called This Function from "Get Posts API"
        if isinstance(post, list):
            # Add Into Cached Posts ALL User Posts
            cached_posts: list[dict] = post

        # Update Cache
        await cache.set(cache_key, cached_posts)

    return cached_posts


async def delete_post_from_cache(
        user_email: str,
        post_id: int
) -> None:
    """
    Update Cached Posts List Without Deleted Post
    """

    # Get Cached Posts and Cache Key
    cached_posts, cache_key = await get_cached_posts_and_cache_key(
        user_email=user_email
    )
    cached_posts: list | None
    cache_key: str

    if cached_posts:
        # Create List with Cached Post Without Specific Post
        cached_posts: list = [post for post in cached_posts if post["id"] != post_id]

        # Update Cache
        await cache.set(cache_key, cached_posts)

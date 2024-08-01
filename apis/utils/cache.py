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


async def get_and_add_user_posts_into_cache(
        user_email: str,
        post: Post | list = None
) -> list[dict] | None:
    """
    Get From Cache And Add Posts Into Cache
    """

    # Cache Key for Posts
    cache_key: str = f"{user_email}_posts"

    # Get Cached Posts
    cached_posts: list | None = await cache.get(cache_key, None)

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

        # Get Cached Posts
        await cache.set(cache_key, cached_posts)

    return cached_posts

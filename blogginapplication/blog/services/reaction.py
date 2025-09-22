from django.db import transaction
from django.contrib.auth import get_user_model
from ..models import Post, PostLike, Bookmark
from ..exceptions import NotFoundError

User = get_user_model()


def _get_post(pk: int) -> Post:
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise NotFoundError("Post not found.")


def like_post(*, user, post_id: int) -> None:
    post = _get_post(post_id)
    PostLike.objects.get_or_create(user=user, post=post)


def unlike_post(*, user, post_id: int) -> None:
    post = _get_post(post_id)
    PostLike.objects.filter(user=user, post=post).delete()


def bookmark_post(*, user, post_id: int) -> None:
    post = _get_post(post_id)
    Bookmark.objects.get_or_create(user=user, post=post)


def remove_bookmark_post(*, user, post_id: int) -> None:
    post = _get_post(post_id)
    Bookmark.objects.filter(user=user, post=post).delete()

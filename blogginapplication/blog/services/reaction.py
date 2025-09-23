# from django.db import transaction
from ..models import PostLike, Bookmark, CommentLike
from .post import _get_post
from .comment import _get_comment

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


def like_comment(*, user, comment_id: int) -> None:
    comment = _get_comment(comment_id)
    CommentLike.objects.get_or_create(user=user, comment=comment)


def unlike_comment(*, user, comment_id: int) -> None:
    comment = _get_comment(comment_id)
    CommentLike.objects.filter(user=user, comment=comment).delete()

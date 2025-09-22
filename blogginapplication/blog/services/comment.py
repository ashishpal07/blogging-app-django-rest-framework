from django.db import transaction
from django.contrib.auth import get_user_model
from ..models import Comment, Post, CommentStatus
from ..exceptions import NotFoundError, PermissionError, ValidationError

User = get_user_model()


def _get_comment(pk: int) -> Comment:
    try:
        return Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        raise NotFoundError("Comment not found.")


def _get_post(pk: int) -> Post:
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise NotFoundError("Post not found.")


def create_comment(
    *, author, post_id: int, parent_id: int | None = None, body: str
) -> Comment:
    post = _get_post(post_id)
    body = (body or "").strip()
    if not body:
        raise ValidationError("comment body is required.")
    parent = None
    if parent_id:
        parent = _get_comment(parent_id)
        if parent.parent_id:
            raise ValidationError("cannot reply to a reaply comment.")
        if parent.post_id != post_id:
            raise ValidationError("parent comment does not belong to the same post.")
    return Comment.objects.create(
        post=post, author=author, parent=parent, body=body, status=CommentStatus.VISIBLE
    )


def update_comment(*, author, comment_id: int, body: str) -> Comment:
    comment = _get_comment(comment_id)
    if comment.author_id != author.id and not (author.is_staff or author.is_superuser):
        raise PermissionError("You do not have permission to modify this comment.")
    body = (body or "").strip()
    if not body:
        raise ValidationError("comment body is required.")
    comment.body = body
    comment.save()
    return comment


@transaction.atomic
def delete_comment(*, user, comment_id: int) -> None:
    comment = _get_comment(comment_id)
    if comment.author_id != user.id and not (user.is_staff or user.is_superuser):
        raise PermissionError("Only author or admin can delete.")
    comment.delete()

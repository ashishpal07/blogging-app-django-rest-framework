from typing import Optional
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


def unique_slugify(
    model, base_text: str, slug_field: str = "slug", max_length: int = 201
) -> str:
    base = slugify(base_text)[:max_length] or "item"
    slug = base
    i = 2

    while model.objects.filter(**{slug_field: slug}).exists():
        suffix = f"-{i}"
        slug = (base[: max_length - len(suffix)]) + suffix
        i += 1
    return slug


def auth_user(request, message: str = "Authentication required."):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        raise ValidationError(message)
    return user


def is_liked_by_user(
    user, *, post_id: Optional[int] = None, comment_id: Optional[int] = None
) -> bool:
    if not user or not user.is_authenticated:
        return False

    if post_id is not None:
        from ..models import PostLike

        return PostLike.objects.filter(user=user, post_id=post_id).exists()
    if comment_id is not None:
        from ..models import CommentLike

        return CommentLike.objects.filter(user=user, comment_id=comment_id).exists()
    return False


def is_bookmarked_by_user(user, *, post_id: Optional[int] = None):
    if not user or not user.is_authenticated:
        return False

    if post_id is not None:
        from ..models import Bookmark

        return Bookmark.objects.filter(user=user, post_id=post_id).exists()
    return False


def make_excerpt(text: str, length: int = 160) -> str:
    text = (text or "").strip()
    return (text[:length] + "...") if len(text) > length else text

def _slug_ok(slug: str) -> str:
    slug = (slug or "").strip().lower()
    if not slug:
        raise ValidationError("slug is required.")
    return slug

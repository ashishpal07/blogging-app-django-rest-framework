from django.contrib.auth import get_user_model
from django.db import transaction
from ..models import Post, Category, Tag, PostStatus
from ..exceptions import ValidationError, NotFoundError, DomainError
from ..utility.utils import unique_slugify
from django.utils import timezone


User = get_user_model()


def _get_post(pk: int) -> Post:
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise NotFoundError("Post with id {pk} not found.")
    return post


def _ensure_publishable(data: dict | None, current: Post | None = None):
    if not data:
        data = {}
    status = data.get("status", getattr(current, "status", None))
    body = data.get("body", getattr(current, "body", None))

    if isinstance(body, str):
        body = body.strip()
    if status == PostStatus.PUBLISHED and not body:
        raise ValidationError("Published post must have body.")


def _check_author(user, post):
    if not user or not user.is_authenticated:
        raise DomainError("UNAUTHORIZED", "Authentication required.")
    if not (user.is_staff or post.author_id == user.id):
        raise DomainError("FORBIDDEN", "You do not have permission to modify this post.")


@transaction.atomic
def create_post(*, author, data: dict) -> Post:
    _ensure_publishable(data, None)

    tags_slugs = data.pop("tags", [])
    cat_slug = data.pop("category", None)

    if "slug" not in data or not (data.get("slug") or "").strip():
        data["slug"] = unique_slugify(Post, data["title"])

    category = None
    if cat_slug:
        try:
            category = Category.objects.get(slug=cat_slug)
        except Category.DoesNotExist:
            raise ValidationError(f"Category with slug {cat_slug} does not exist.")

    post = Post.objects.create(author=author, category=category, **data)

    if tags_slugs:
        tags = list(Tag.objects.filter(slug__in=tags_slugs))
        if len(tags) != len(set(tags_slugs)):
            missing = sorted(set(tags_slugs) - set(t.slug for t in tags))
            raise ValidationError(f"Tags with slugs {", ".join(missing)} do not exist.")

        post.tags.set(tags)

    return post


@transaction.atomic
def update_post(*, user, post_id: int, data: dict) -> Post:
    post = _get_post(post_id)
    _check_author(user, post)

    tags_slugs = data.pop("tags", None)
    cat_slug = data.pop("category", None)

    if "slug" in data and (data["slug"] or "").strip() == "":
        data["slug"] = unique_slugify(Post, data.get("title", post.title))

    new_status = data.get("status", post.status)
    new_body = data.get("body", post.body)

    if new_status == PostStatus.PUBLISHED and not (new_body or "").strip():
        raise DomainError("VALIDATION", "Published post must have body.")

    for k, v in data.items():
        setattr(post, k, v)

    if cat_slug is not None:
        if cat_slug == "" or cat_slug is None:
            post.category = None
        else:
            try:
                post.category = Category.objects.get(slug=cat_slug)
            except Category.DoesNotExist:
                raise DomainError("NOT_FOUND", f"Category with slug '{cat_slug}' does not exist.")

    if new_status == PostStatus.PUBLISHED:
        if not post.published_at:
            post.published_at = timezone.now()
    else:
        post.published_at = None

    post.save()

    if tags_slugs is not None:
        if len(tags_slugs) == 0:
            post.tags.clear()
        else:
            tags = list(Tag.objects.filter(slug__in=tags_slugs))
            found_slugs = {t.slug for t in tags}
            missing = [s for s in tags_slugs if s not in found_slugs]
            if missing:
                raise DomainError("NOT_FOUND", f"Tags not found: {', '.join(missing)}")
            post.tags.set(tags)
    return post

@transaction.atomic
def publish_post(*, user, post_id: int) -> Post:
    post = _get_post(post_id)
    _check_author(user, post)
    _ensure_publishable({"status": PostStatus.PUBLISHED, "body": post.body}, post)
    post.status = PostStatus.PUBLISHED
    post.published_at = timezone.now()
    post.save()
    return post

@transaction.atomic
def unpublish_post(*, user, post_id: int) -> Post:
    post = _get_post(post_id)
    _check_author(user, post)
    post.status = PostStatus.DRAFT
    post.save()
    return post

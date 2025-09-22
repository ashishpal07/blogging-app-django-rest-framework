from django.contrib.auth import get_user_model
from django.db import transaction
from ..models import Post, Category, Tag, PostStatus
from ..exceptions import ValidationError, NotFoundError
from ..utility.utils import unique_slugify

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


def _check_author(author, obj: Post):
    if obj.author_id != author.id:
        raise PermissionError("You do not have permission to modify this post.")


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
    _ensure_publishable(data, post)

    tags_slugs = data.pop("tags", None)
    cat_slug = data.pop("category", None)

    if "slug" in data and (data["slug"] or "").strip() == "":
        data["slug"] = unique_slugify(Post, data.get("title", post.title))

    for k, v in data.items():
        setattr(post, k, v)

    if cat_slug is not None:
        if cat_slug == "":
            post.category = None
        else:
            try:
                post.category = Category.objects.get(slug=cat_slug)
            except Category.DoesNotExist:
                raise ValidationError(f"Category '{cat_slug}' does not exist.")

    post.save()

    if tags_slugs is not None:
        if len(tags_slugs) == 0:
            post.tags.clear()
        else:
            tags = list(Tag.objects.filter(slug__in=tags_slugs))
            if len(tags) != len(tags_slugs):
                missing = sorted(set(tags_slugs) - set(t.slug for t in tags))
                raise ValidationError(f"Tags not found: {', '.join(missing)}")
            post.tags.set(tags)

    return post

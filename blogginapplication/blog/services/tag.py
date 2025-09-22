from ..models import Tag
from ..exceptions import NotFoundError, ValidationError
from ..utility.utils import _slug_ok


def create_tag(*, name: str, slug: str) -> Tag:
    slug = _slug_ok(slug)

    if Tag.objects.filter(slug__iexact=slug).exists():
        raise ValidationError(f"Tag with slug {slug} already exists.")

    tag = Tag.objects.create(name=name.strip(), slug=slug)
    return tag


def update_tag(*, tag_id: int, data: dict) -> Tag:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        raise NotFoundError(f"Tag with id {tag_id} not found.")

    if "name" in data:
        tag.name = data["name"].strip()

    if "slug" in data:
        new_slug = _slug_ok(data["slug"])
        if new_slug != tag.slug and Tag.objects.filter(slug__iexact=new_slug).exists():
            raise ValidationError(f"Tag with slug {new_slug} already exists.")
        tag.slug = new_slug
    tag.save()
    return tag


def delete_tag(*, slug: str) -> None:
    try:
        tag = Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        raise NotFoundError(f"Tag with slug {slug} not found.")
    tag.delete()


def delete_tag_by_id(*, tag_id: int) -> None:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        raise NotFoundError(f"Tag with id {tag_id} not found.")
    tag.delete()

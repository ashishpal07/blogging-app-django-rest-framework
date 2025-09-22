# from django.db import transaction
from ..models import Category
from ..exceptions import ValidationError, NotFoundError
from ..utility.utils import _slug_ok


def create_category(*, name: str, slug: str) -> Category:
    slug = _slug_ok(slug)
    if Category.objects.filter(slug__iexact=slug).exists():
        raise ValidationError(f"Category with slug {slug} already exists.")
    category = Category.objects.create(name=name.strip(), slug=slug)
    return category


def update_category(*, category_id: int, data: dict) -> Category:
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFoundError(f"Category with id {category_id} not found.")

    if "name" in data:
        category.name = data["name"].strip()
    if "slug" in data:
        new_slug = _slug_ok(data["slug"])
        if (
            new_slug != category.slug
            and Category.objects.filter(slug__iexact=new_slug).exists()
        ):
            raise ValidationError(f"Category with slug {new_slug} already exists.")
        category.slug = new_slug
    category.save()
    return category


def delete_category(*, slug: str) -> None:
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise NotFoundError(f"Category with slug {slug} not found.")
    category.delete()


def delete_category_by_id(*, category_id: int) -> None:
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise NotFoundError(f"Tag with id {category_id} not found.")
    category.delete()

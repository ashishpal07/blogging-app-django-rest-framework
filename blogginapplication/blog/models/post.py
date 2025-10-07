from django.db import models
from .common import TimestampedModel
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from .tag import Tag


class PostStatus(models.TextChoices):
    DRAFT = (
        "DRAFT",
        "Draft",
    )
    PUBLISHED = (
        "PUBLISHED",
        "Published",
    )
    ARCHIVED = (
        "ARCHIVED",
        "Archived",
    )


class Post(TimestampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    body = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        db_index=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    class Meta:
        db_table = "blog_post"
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["author", "created_at"]),
        ]
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:80]
            self.slug = base
        if self.status == PostStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"

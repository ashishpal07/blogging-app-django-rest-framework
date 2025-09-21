from django.db import models
from .common import TimestampedModel
from django.utils.text import slugify


class Category(TimestampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.CharField(max_length=90, unique=True)

    class Meta:
        db_table = "blog_category"
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:90]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

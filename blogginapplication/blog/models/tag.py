from django.db import models
from .common import TimestampedModel
from django.utils.text import slugify

class Tag(TimestampedModel):
  name = models.CharField(max_length=50, unique=True)
  slug = models.CharField(max_length=60, unique=True)

  class Meta:
    db_table = 'blog_tag'
    indexes = [models.Index(fields=['slug'])]

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)[:60]
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name

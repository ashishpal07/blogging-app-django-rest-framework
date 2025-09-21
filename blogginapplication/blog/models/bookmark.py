from django.db import models
from .common import TimestampedModel
from django.conf import settings
from .post import Post

class Bookmark(TimestampedModel):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_bookmark")

  class Meta:
    db_table = "blog_bookmark"
    constraints = [
      models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_bookmark")
    ]
    indexes = [
      models.Index(fields=["user"]),
      models.Index(fields=["post"])
    ]
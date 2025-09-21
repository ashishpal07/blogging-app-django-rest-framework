from django.db import models
from .common import TimestampedModel
from .comment import Comment
from django.conf import settings

class CommentLike(TimestampedModel):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes")

  class Meta:
    db_table = "blog_comment_like"
    constraints = [
      models.UniqueConstraint(fields=["comment", "user"], name="unique_user_comment_like")
    ]
    indexes = [
      models.Index(fields=["comment"]),
      models.Index(fields=["user"]),
    ]

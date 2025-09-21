from django.db import models
from .common import TimestampedModel
from .post import Post
from django.conf import settings


class CommentStatus(models.TextChoices):
    VISIBLE = "VISIBLE", "Visible"
    HIDDEN = "HIDDEN", "Hidden"
    PENDING = "PENDING", "Pending"


class Comment(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    body = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=CommentStatus.choices,
        default=CommentStatus.VISIBLE,
        db_index=True,
    )

    class Meta:
        db_table = 'blog_comment'
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['status']),
        ]
    def __str__(self):
        return f"{self.pk} on {self.post_id}"
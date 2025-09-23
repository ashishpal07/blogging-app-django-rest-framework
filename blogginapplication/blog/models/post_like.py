from django.db import models
from .common import TimestampedModel
from .post import Post
from django.conf import settings


class PostLike(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes"
    )

    class Meta:
        db_table = "blog_post_like"
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")
        ]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]


# foreign key
# group by, order by,

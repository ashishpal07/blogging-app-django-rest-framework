from django.db import models
from .common import TimestampedModel
from .tag import Tag
from .post import Post


class PostTag(TimestampedModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="post_tags")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tag_posts")

    class Meta:
        db_table = "blog_post_tag"
        constraints = [
            models.UniqueConstraint(fields=["tag", "post"], name="unique_tag_post")
        ]
        indexes = [
            models.Index(fields=["tag"]),
            models.Index(fields=["post"]),
        ]

    def __str__(self):
        return f"{self.post_id} --> {self.tag_id}"

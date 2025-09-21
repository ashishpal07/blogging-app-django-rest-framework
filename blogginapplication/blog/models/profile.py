from django.db import models
from .common import TimestampedModel
from django.conf import settings


class Profile(TimestampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    class Meta:
        db_table = "blog_profile"

    def __str__(self):
        return self.display_name or self.user.username

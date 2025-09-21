from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    logger.info(f"create_profile signal fired for {instance.username}")
    if created:
        Profile.objects.create(user=instance)

from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Profile, Category, Tag


User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("user", "display_name", "bio", "avatar", "created_at", "updated_at")
        read_only_fields = fields


class ProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Profile
        fields = ("display_name", "bio", "avatar")
        extra_kwargs = {"avatar": {"required": False}}

    def validate_avatar(self, file):
        # size check
        max_mb = 5
        if file.size > max_mb * 1024 * 1024:
            raise serializers.ValidationError(f"Max file size {max_mb}MB allowed.")
        # type check
        allowed = {"image/jpeg", "image/png", "image/webp"}
        content_type = getattr(file, "content_type", None)
        if content_type and content_type not in allowed:
            raise serializers.ValidationError("Only JPEG/PNG/WEBP allowed.")
        return file



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug", "created_at", "updated_at")

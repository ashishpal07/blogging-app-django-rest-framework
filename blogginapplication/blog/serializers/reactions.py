from rest_framework import serializers
from ..models import PostLike, CommentLike, Bookmark
from ..utility.utils import auth_user


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("post",)

    def create(self, validated):
        user = auth_user(self.context["request"])
        like, _ = PostLike.objects.get_or_create(user=user, post=validated["post"])
        return like


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ("comment",)

    def create(self, validated):
        user = auth_user(self.context["request"])
        like, _ = CommentLike.objects.get_or_create(
            user=user, comment=validated["comment"]
        )
        return like


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("post",)

    def create(self, validated):
        user = auth_user(self.context["request"])
        bm, _ = Bookmark.objects.get_or_create(user=user, post=validated["post"])
        return bm

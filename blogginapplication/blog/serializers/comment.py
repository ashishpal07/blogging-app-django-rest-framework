from django.db.models import Count
from rest_framework import serializers
from ..models import Comment, CommentStatus
from .common import UserMiniSerializer
from ..utility.utils import is_liked_by_user
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class CommentReplySerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "parent",
            "body",
            "status",
            "created_at",
            "updated_at",
            "like_count",
            "is_liked_by_me",
        )
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_liked_by_me(self, obj):
        req = self.context.get("request")
        return is_liked_by_user(getattr(req, "user", None), comment_id=obj.id)


class CommentReadSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked_by_me = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "parent",
            "body",
            "status",
            "created_at",
            "updated_at",
            "like_count",
            "is_liked_by_me",
            "replies",
        )
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_liked_by_me(self, obj):
        req = self.context.get("request")
        return is_liked_by_user(getattr(req, "user", None), comment_id=obj.id)

    @extend_schema_field(CommentReplySerializer(many=True))
    def get_replies(self, obj):
        qs = (
            obj.replies.filter(status=CommentStatus.VISIBLE)
            .select_related("author")
            .annotate(like_count=Count("likes"))
        )
        return CommentReplySerializer(qs, many=True, context=self.context).data


class CommentWriteSerializer(serializers.Serializer):
    post = serializers.IntegerField()
    parent = serializers.IntegerField(required=False, allow_null=True)
    body = serializers.CharField()

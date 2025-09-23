from rest_framework import serializers
from django.db import transaction
from django.db.models import Count

from ..models import Post, PostStatus, CommentStatus

from .common import UserMiniSerializer, CategorySerializer, TagSerializer
from .comment import CommentReadSerializer
from ..utility.utils import (
    is_liked_by_user,
    is_bookmarked_by_user,
    make_excerpt,
)

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class PostListSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    like_count = serializers.IntegerField(read_only=True, default=0)
    comment_count = serializers.IntegerField(read_only=True, default=0)

    is_liked_by_me = serializers.SerializerMethodField()
    is_bookmarked_by_me = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "is_liked_by_me",
            "is_bookmarked_by_me",
            "excerpt",
            "author",
            "title",
            "category",
            "tags",
            "like_count",
            "comment_count",
            "created_at",
            "updated_at",
            "status",
            "published_at",
            "slug",
        )

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_liked_by_me(self, obj):
        req = self.context.get("request")
        return is_liked_by_user(getattr(req, "user", None), post_id=obj.id)

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_bookmarked_by_me(self, obj):
        req = self.context.get("request")
        return is_bookmarked_by_user(getattr(req, "user", None), post_id=obj.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_excerpt(self, obj) -> str:
        return make_excerpt(obj.body)


class PostDetailsSerializer(PostListSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = PostListSerializer.Meta.fields + ("comments",)

    @extend_schema_field(CommentReadSerializer(many=True))
    def get_comments(self, obj):
        qs = (
            obj.comments.filter(parent__isnull=True, status=CommentStatus.VISIBLE)
            .select_related("author")
            .annotate(like_count=Count("likes"))
        )
        return CommentReadSerializer(qs, many=True, context=self.context).data


class PostWriteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(allow_blank=True, required=False)
    category = serializers.SlugField(required=False, allow_null=True, allow_blank=True)
    tags = serializers.ListField(child=serializers.SlugField(), required=False)
    status = serializers.ChoiceField(choices=PostStatus.choices, required=False)
    slug = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        status = attrs.get("status")
        body = attrs.get("body", "")
        if status == PostStatus.PUBLISHED and not (body or "").strip():
            raise serializers.ValidationError("Published post must have body.")
        return attrs

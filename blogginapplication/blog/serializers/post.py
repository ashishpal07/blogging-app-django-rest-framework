from rest_framework import serializers
from django.db import transaction
from django.db.models import Count
from rest_framework.validators import UniqueValidator

from ..models import Category, Post, Tag, PostStatus, CommentStatus

from .common import UserMiniSerializer, CategorySerializer, TagSerializer
from .comment import CommentReadSerializer
from ..utility.utils import (
    auth_user,
    unique_slugify,
    is_liked_by_user,
    is_bookmarked_by_user,
    make_excerpt,
)

from drf_spectacular.utils import extend_schema_field, OpenApiTypes

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

    def get_excerpt(self, obj):
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


class PostWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
        allow_null=True,
        required=False,
    )

    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), slug_field="slug", many=True, required=False
    )

    slug = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=Post.objects.all())],
    )

    class Meta:
        model = Post
        fields = ("title", "body", "category", "tags", "status", "slug")

    def validate_status(self, value):
        if value not in dict(PostStatus.choices):
            raise serializers.ValidationError("Invalid status")
        return value;

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        
        new_status = attrs.get("status", getattr(instance, "status", None))
        new_body = attrs.get("body", getattr(instance, "body", None))
        
        if isinstance(new_body, str):
            new_body = new_body.strip()

        if new_status == PostStatus.PUBLISHED and not new_body:
            raise serializers.ValidationError("Published post must have body.")
        
        return attrs

    @transaction.atomic
    def create(self, validated):
        user = auth_user(self.context.get("request"))
        tags = validated.pop("tags", [])
        if not validated.get("slug"):
            validated["slug"] = unique_slugify(Post, validated.get("title"))
        post  = Post.objects.create(author=user, **validated)
        if tags:
            post.tags.set(tags)
        return post

    @transaction.atomic
    def update(self, instance, validated):
        tags = validated.pop("tags", [])
        if "slug" in validated and validated["slug"] == "":
            validated["slug"] = unique_slugify(Post, validated.get("title", instance.title))

        for k, v in validated.items():
            setattr(instance, k, v)
        instance.save()

        if tags:
            instance.tags.set(tags)
        return instance

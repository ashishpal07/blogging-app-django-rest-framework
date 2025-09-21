from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from django.utils import timezone
from django.db.models import Count, Q

from ..models import Post, PostLike, PostStatus, Bookmark, CommentStatus

from ..serializers import PostDetailsSerializer, PostListSerializer, PostWriteSerializer

from ..permissions import IsAuthOrReadOnly
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from ..filter import PostFilter


class PostViewSet(viewsets.ModelViewSet):
    print("Post view set initialized")
    filterset_class = PostFilter
    permission_classes = [IsAuthOrReadOnly, IsAuthenticatedOrReadOnly, IsAuthenticated]
    throttle_scope = None

    def get_queryset(self):
        print("Fetching queryset for postviewset")
        qs = (
            Post.objects.select_related("author", "category")
            .prefetch_related("tags")
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__status=CommentStatus.VISIBLE),
                    distinct=True,
                ),
            )
        )

        params = self.request.query_params
        status_param = params.get("status")

        if status_param:
            qs = qs.filter(status=status_param)

        category = params.get("category")
        if category:
            qs.filter(category__slug=category)

        author = params.get("author")
        if author:
            qs.filter(author__username=author)

        tags = params.get("tags")
        if tags:
            slugs = [t.strip() for t in tags.split(",") if t.strip()]
            print("slugs:", slugs)
            if slugs:
                qs = qs.filter(tags__slug__in=slugs).distinct()

        published_from = params.get("published_from")
        published_to = params.get("published_to")
        if published_from:
            qs = qs.filter(published_at__date__gte=published_from)
        if published_to:
            qs = qs.filter(published_at__date__lte=published_to)

        return qs

    search_fields = ["title", "body"]
    ordering_fields = ["published_at", "like_count", "comment_count", "created_at"]
    ordering = ["-published_at", "-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailsSerializer
        return PostWriteSerializer

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="PublishResponse",
            fields={
                "status": serializers.CharField(),
                "published_at": serializers.DateTimeField(allow_null=True),
            },
        ),
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        throttle_scope="write",
    )
    def publish(self, request, pk=None):
        post = self.get_object()
        post.status = PostStatus.PUBLISHED

        if not post.published_at:
            post.published_at = timezone.now()
        post.save(update_fields=["status", "published_at", "updated_at"])

        return Response({"status": "Published", "published_at": post.published_at})

    @action(
        detail=True,
        methods=["post"],
        url_path="unpublish",
        permission_classes=[IsAuthenticated],
        throttle_scope="write",
    )
    def unpublished(self, request, pk=None):
        post = self.get_object()
        post.status = PostStatus.DRAFT
        post.save(update_fields=["status", "updated_at"])

        return Response({"status": "draft"})

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="LikeResponse", fields={"liked": serializers.BooleanField()}
        ),
    )
    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        throttle_scope="write",
    )
    def like(self, request, pk=None):
        post = self.get_object()
        if request.method.lower() == "post":
            PostLike.objects.get_or_create(user=request.user, post=post)
            return Response({"liked": True}, status=status.HTTP_201_CREATED)
        PostLike.objects.filter(user=request.user, post=post).delete()
        return Response({"liked": False}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="BookmarkResponse", fields={"bookmarked": serializers.BooleanField()}
        ),
    )
    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        throttle_scope="write",
    )
    def bookmark(self, request, pk=None):
        post = self.get_object()
        if request.method.lower() == "post":
            Bookmark.objects.get_or_create(user=request.user, post=post)
            return Response({"bookmarked": True}, status=status.HTTP_201_CREATED)
        Bookmark.objects.filter(user=request.user, post=post).delete()
        return Response({"bookmarked": False}, status=status.HTTP_204_NO_CONTENT)

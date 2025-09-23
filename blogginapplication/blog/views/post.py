from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from django.db.models import Count

from ..models import Post

from ..serializers import PostDetailsSerializer, PostListSerializer, PostWriteSerializer

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from ..services import (
    create_post,
    bookmark_post,
    remove_bookmark_post,
    publish_post,
    like_post,
    unlike_post,
    unpublish_post,
    update_post,
)
from ..exceptions import DomainError, raise_api_for
# from ..filter import PostFilter


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = (
        Post.objects.all()
        .select_related("author", "category")
        .prefetch_related("tags")
        .annotate(like_count=Count("likes"), comment_count=Count("comments"))
    )
    lookup_field = "id"

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
    def create(self, request, *args, **kwargs):
        serializer = PostWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        try:
            post = create_post(
                author=request.user, data=serializer.validated_data.copy()
            )
        except DomainError as e:
            raise_api_for(e)
        post = PostDetailsSerializer(post, context={"request": request}).data
        return Response(post, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = PostWriteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            post = update_post(
                user=request.user,
                post_id=kwargs["id"],
                data=serializer.validated_data.copy()
            )
        except DomainError as e:
            raise_api_for(e)
        return Response(PostDetailsSerializer(post, context={"request": request}).data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def publish(self, request, id=None):
        try:
            post = publish_post(user=request.user, post_id=id)
        except DomainError as e:
            raise_api_for(e)
        return Response(PostDetailsSerializer(post, context={"request": request}).data)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def unpublished(self, request, id=None):
        try:
            post = unpublish_post(user=request.user, post_id=id)
        except DomainError as e:
            raise_api_for(e)
        return Response(PostDetailsSerializer(post, context={"request": request}).data)

    @action(
        methods=["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def like(self, request, id=None):
        try:
            if request.method.lower() == "post":
                like_post(user=request.user, post_id=id)
                return Response({"status": "liked"})
            else:
                unlike_post(user=request.user, post_id=id)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except DomainError as e:
            raise_api_for(e)

    @action(
        methods=["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, id=None):
        try:
            if request.method.lower() == "post":
                bookmark_post(user=request.user, post_id=id)
                return Response({"status": "bookmarked"})
            else:
                remove_bookmark_post(user=request.user, post_id=id)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except DomainError as e:
            raise_api_for(e)

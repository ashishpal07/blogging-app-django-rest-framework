from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Comment
from ..serializers import CommentReadSerializer, CommentWriteSerializer
from ..permissions import IsAuthOrReadOnly

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from ..models import CommentLike


class CommentViewSet(viewsets.ModelViewSet):
    throttle_scope = None
    permission_classes = [IsAuthOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post", "parent").annotate(
            like_count=Count("likes", distinct=True)
        )

        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        param_status = self.request.query_params.get("status")
        if param_status:
            qs = qs.filter(status=param_status)

        return qs.order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CommentWriteSerializer
        return CommentReadSerializer
    
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
        comment = self.get_object()
        if request.method.lower() == "post":
            CommentLike.objects.get_or_create(user=request.user, comment=comment)
            return Response({"liked": True}, status=status.HTTP_201_CREATED)
        CommentLike.objects.filter(user=request.user, comment=comment).delete()
        return Response({"liked": False}, status=status.HTTP_204_NO_CONTENT)

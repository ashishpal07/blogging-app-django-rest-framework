from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Comment
from ..serializers import CommentReadSerializer, CommentWriteSerializer
from ..permissions import IsAuthOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
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

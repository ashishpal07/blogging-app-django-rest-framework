from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers import CommentWriteSerializer, CommentReadSerializer
from ..models import Comment, CommentStatus
from django.db.models import Count
from ..services import create_comment, update_comment, delete_comment
from ..exceptions import DomainError, raise_api_for

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.all().select_related("author","post","parent").annotate(
        like_count=Count("likes")
    )

    def get_serializer_class(self):
        if self.action in ("list","retrieve"):
            return CommentReadSerializer
        return CommentWriteSerializer

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get("post")
        qs = self.get_queryset()
        if post_id:
            qs = qs.filter(post_id=post_id, parent__isnull=True, status=CommentStatus.VISIBLE)
        data = CommentReadSerializer(qs, many=True, context={"request": request}).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        ser = CommentWriteSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        try:
            comment = create_comment(
                author=request.user,
                post_id=ser.validated_data["post"],
                body=ser.validated_data["body"],
                parent_id=ser.validated_data.get("parent"),
            )
        except DomainError as e:
            raise_api_for(e)
        return Response(CommentReadSerializer(comment, context={"request": request}).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        ser = CommentWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            comment = update_comment(user=request.user, comment_id=comment_id, body=ser.validated_data["body"])
        except DomainError as e:
            raise_api_for(e)
        return Response(CommentReadSerializer(comment, context={"request": request}).data)

    def destroy(self, request, *args, **kwargs):
        cid = kwargs.get("pk")
        try:
            delete_comment(user=request.user, comment_id=cid)
        except DomainError as e:
            raise_api_for(e)
        return Response(status=status.HTTP_204_NO_CONTENT)

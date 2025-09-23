from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers.common import CategorySerializer, TagSerializer
from ..models import Category, Tag
from ..permissions import IsAdminOrReadOnly
from ..services import create_category, update_category, delete_category, create_tag, update_tag, delete_tag
from ..exceptions import DomainError, raise_api_for

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        ser = CategorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            obj = create_category(**ser.validated_data)
        except DomainError as e:
            raise_api_for(e)
        return Response(CategorySerializer(obj).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        ser = CategorySerializer(data=request.data, partial=(request.method=="PATCH"))
        ser.is_valid(raise_exception=True)
        try:
            obj = update_category(slug=slug, data=ser.validated_data)
        except DomainError as e:
            raise_api_for(e)
        return Response(CategorySerializer(obj).data)

    def destroy(self, request, *args, **kwargs):
        try:
            delete_category(slug=kwargs.get("slug"))
        except DomainError as e:
            raise_api_for(e)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        ser = TagSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            obj = create_tag(**ser.validated_data)
        except DomainError as e:
            raise_api_for(e)
        return Response(TagSerializer(obj).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        ser = TagSerializer(data=request.data, partial=(request.method=="PATCH"))
        ser.is_valid(raise_exception=True)
        try:
            obj = update_tag(slug=slug, data=ser.validated_data)
        except DomainError as e:
            raise_api_for(e)
        return Response(TagSerializer(obj).data)

    def destroy(self, request, *args, **kwargs):
        try:
            delete_tag(slug=kwargs.get("slug"))
        except DomainError as e:
            raise_api_for(e)
        return Response(status=status.HTTP_204_NO_CONTENT)

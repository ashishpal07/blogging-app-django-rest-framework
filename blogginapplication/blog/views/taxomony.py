from rest_framework import viewsets
from ..models import Category, Tag
from ..serializers import CategorySerializer, TagSerializer
from ..permissions import IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"  # better UX: /categories/python/

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def perform_create(self, serializer):
        obj = serializer.save() 

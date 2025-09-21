
import django_filters as df
from .models import Post

class PostFilter(df.FilterSet):
    status = df.CharFilter(field_name="status")
    category = df.CharFilter(field_name="category__slug")
    author = df.CharFilter(field_name="author__username")
    tags = df.CharFilter(method="filter_tags")
    published_from = df.DateFilter(field_name="published_at", lookup_expr="date__gte")
    published_to   = df.DateFilter(field_name="published_at", lookup_expr="date__lte")

    def filter_tags(self, qs, name, value):
        slugs = [s.strip() for s in value.split(",") if s.strip()]
        return qs.filter(tags__slug__in=slugs).distinct()

    class Meta:
        model = Post
        fields = ["status", "category", "author", "tags", "published_from", "published_to"]

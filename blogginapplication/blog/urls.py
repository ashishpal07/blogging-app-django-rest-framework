from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.post import PostViewSet
from .views.comment import CommentViewSet
from .views.taxomony import CategoryViewSet, TagViewSet
from .views.profile import MeProfileView
from .views.auth import RegisterView, MeView, ChangePasswordView

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
    path("me/profile/", MeProfileView.as_view(), name="me-profile"),

    path("register/", RegisterView.as_view(), name="register"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
]

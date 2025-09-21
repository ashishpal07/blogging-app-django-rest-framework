from rest_framework import permissions

class IsAuthOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    author = getattr(obj, "author", None)
    return author == getattr(request, "user", None)


class IsAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return bool(request.user and request.user.is_staff)

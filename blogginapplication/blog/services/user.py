from django.contrib.auth import get_user_model
from django.db import transaction
from ..exceptions import ValidationError

User = get_user_model()


def register_user(
    *,
    username: str,
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
):
    username = (username or "").strip()
    if not username:
        raise ValidationError("username is required.")
    email = (email or "").strip()
    if not email:
        raise ValidationError("email is required.")

    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError(f"username {username} is already taken.")

    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError(f"email {email} is already taken.")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
    )
    return user

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import (
    RegisterSerializer,
    UserMeSerializer,
    ChangePasswordSerializer,
    RegisterResponseSerializer,
    ChangePasswordOKSerializer,
)
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer, responses={201: RegisterResponseSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserMeSerializer})
    def get(self, request):
        return Response(UserMeSerializer(request.user).data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer, responses={200: ChangePasswordOKSerializer}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not check_password(old_password, request.user.password):
            return Response(
                {"old_password": "Old password is not correct."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save(update_fields=["password"])

        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )

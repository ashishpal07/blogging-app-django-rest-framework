from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.common import ProfileSerializer, ProfileUpdateSerializer

from drf_spectacular.utils import extend_schema

class MeProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(responses=ProfileSerializer)
    def get(self, request):
        prof = request.user.profile
        return Response(ProfileSerializer(prof).data)

    @extend_schema(request=ProfileUpdateSerializer, responses=ProfileSerializer)
    def patch(self, request):
        prof = request.user.profile
        ser = ProfileUpdateSerializer(prof, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ProfileSerializer(prof).data)

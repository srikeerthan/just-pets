# Create your views here.
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView

from .models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes


@permission_classes((AllowAny,))
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class AccountsDetailView(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        user_obj = User.objects.get(email=kwargs.get("email"))
        data = {
            'email': user_obj.email,
            'username': user_obj.username,
            "created_time": user_obj.created_at
        }
        return Response(data, status=status.HTTP_200_OK)

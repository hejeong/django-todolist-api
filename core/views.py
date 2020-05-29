from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from django.db import IntegrityError

from .serializers import UserSerializer, CustomTokenObtainPairSerializer


# helper method for manual creation of JWT tokens


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def check_user_token(request):
    # if the token is not valid, an invalid token response is automatically returned
    token = authentication.JWTAuthentication().get_validated_token(request.data['token'])
    # however, if valid token, proceed to find the user
    user = authentication.JWTAuthentication().get_user(token)
    return Response({"username": user.username}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    try:
        user = request.data
        user = User.objects.create_user(
                                    username=user['username'],
                                    password=user['password']
                                )
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"error": "Username is taken. Please choose another."}, status=status.HTTP_409_CONFLICT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
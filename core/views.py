from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.db import IntegrityError


# helper method for manual creation of JWT tokens


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
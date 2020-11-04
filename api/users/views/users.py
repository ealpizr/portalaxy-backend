"""Users views."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from api.users.models.users import User

# Serializers
from api.users.serializers.users import (
    UserModelSerializer,
    UserSignUpSerializer,
    UserLoginSerializer
)


class UserViewSet(viewsets.GenericViewSet):
    """
    User view set.

    Handle sign up and login.
    """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
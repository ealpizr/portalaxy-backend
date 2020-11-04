"""Users serializers."""

# Django
from django.contrib.auth import password_validation, authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from api.users.models import User
from knox.auth import AuthToken

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.

    Handle authentication token creation.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        max_length=64
    )

    def validate(self, data):
        """Check credentials."""
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """Handle token creation."""
        instance, token = AuthToken.objects.create(user=self.context['user'])
        return self.context['user'], token


class UserSignUpSerializer(serializers.Serializer):
    """
    User sign up serializer.

    Handle sign up data validation and user creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        min_length=8,
        max_length=64
    )

    password_confirmation = serializers.CharField(
        min_length=8,
        max_length=64
    )

    first_name = serializers.CharField(
        max_length=30
    )

    last_name = serializers.CharField(
        max_length=30
    )

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        return user
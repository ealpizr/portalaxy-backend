"""Membership serializer."""

# Django REST Framework
from rest_framework import serializers

# Serializer
from api.users.serializers.users import UserModelSerializer

# Models
from api.groups.models import Membership


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = [
            'user',
            'is_admin'
        ]
        read_only_fields = [
            'user'
        ]


class AddMembershipSerializer(serializers.Serializer):
    """
    Add membership serializer.

    Handle the addition of a new member to a group.
    Group object must be provided in the context.
    """

    invitation_code = serializers.CharField(
        min_length=8
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """Verify user isn't already a member."""
        group = self.context['group']
        user = data
        q = Membership.objects.filter(group=group, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already a member of this circle.')
        return data

    def validate_invitation_code(self, data):
        """Verify code exists and that it's related to the group."""
        return data

    def create(self, data):
        group = self.context['group']
        user = data['user']

        member = Membership.objects.create(
            user=user,
            group=group
        )

        return member
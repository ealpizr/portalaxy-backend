"""Group membership views."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from api.groups.models import Group, Membership

# Permissions
from rest_framework.permissions import IsAuthenticated
from api.groups.permissions import IsSelfMember

# Serializers
from api.groups.serializers import MembershipModelSerializer, AddMembershipSerializer


class MembershipViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Group membership view set."""
    serializer_class = MembershipModelSerializer
    lookup_value_regex = r"[-a-zA-Z0-0_.@]+"
    def dispatch(self, request, *args, **kwargs):
        print("dispatch endpoint")
        print(self.kwargs)
        """Verify that the group exists."""
        slug_name = kwargs['slug_name']
        self.group = get_object_or_404(Group, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]

    def get_queryset(self):
        """Return group members."""
        print("endpoint")
        print(self.group)
        return Membership.objects.filter(
            group=self.group
        )
    
    def get_object(self):
        """Return the group member by using the user's email."""
        print(self.kwargs)
        
        return get_object_or_404(
            Membership,
            user__email=self.kwargs['pk'],
            group = self.group
        )

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        return Response('ui')

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMembershipSerializer(
            data=request.data,
            context={'group': self.group, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)
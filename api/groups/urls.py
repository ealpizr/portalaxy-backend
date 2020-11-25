"""Groups URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.groups.views import groups as group_views
from api.groups.views import memberships as membership_views

router = DefaultRouter()
router.register(r'groups', group_views.GroupViewSet, basename='groups')
router.register(
    r'groups/(?P<slug_name>[-a-zA-Z0-0_.@]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)
urlpatterns = [
    path('', include(router.urls))
]
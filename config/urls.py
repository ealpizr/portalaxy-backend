"""Main URLs module."""

# Django
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('api.users.urls', 'users'), namespace='users'))
]

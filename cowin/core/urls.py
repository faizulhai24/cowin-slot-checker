from django.conf.urls import include, url
from rest_framework import routers
from .views import UserViewSet

user_router = routers.SimpleRouter()
user_router.register(r'user', UserViewSet, 'user')

urlpatterns = [
    url(r'^', include(user_router.urls)),
]

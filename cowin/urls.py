from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from cowin.core import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include(user_urls)),
]

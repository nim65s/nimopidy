from django.conf.urls import include, url
from django.contrib import admin

from musicapp.views import SongViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

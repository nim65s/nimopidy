from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from musicapp.views import SongViewSet

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]

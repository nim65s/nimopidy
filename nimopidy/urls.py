from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from musicapp.views import TrackViewSet, webhooks

router = routers.DefaultRouter()
router.register(r'songs', TrackViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^webhooks', webhooks, name='webhooks'),
    url(r'^', include(router.urls)),
]

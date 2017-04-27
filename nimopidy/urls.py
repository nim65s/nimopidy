from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from musicapp.views import SongUpdateView, SongViewSet, lyrics, update_lyrics

router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^lyrics/(?P<uri>.*)$', lyrics, name='lyrics'),
    url(r'^change/(?P<uri>.*)$', SongUpdateView.as_view(), name='change'),
    url(r'^update/(?P<uri>.*)$', update_lyrics, name='update'),
    url(r'^', include(router.urls)),
]

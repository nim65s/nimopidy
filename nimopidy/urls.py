from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from musicapp.views import snapcast, webhooks

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^webhooks', webhooks, name='webhooks'),
    url(r'^snapcast/(?P<target>[0-9a-f:]{17})/(?P<muted>[01])/(?P<percent>[0-9]+)$', snapcast),
]

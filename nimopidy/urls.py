from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from musicapp.views import webhooks

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^webhooks', webhooks, name='webhooks'),
]

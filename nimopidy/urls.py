from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('musicapp.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

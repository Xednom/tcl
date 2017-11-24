from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from tclordering import views


urlpatterns = [
    url(r'^$', views.login_redirect, name='login_redirect'),
    url(r'^tcl-admin/', admin.site.urls),  # original django admin
    url(r'^admin_tools/', include('admin_tools.urls')),  # this is not a replacement for admin just a top layer for it use the original one
    url(r'^ordering/', include('ordering.urls', namespace='ordering')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from mail.views import Index

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico')),
    path('admin/', admin.site.urls),
    path('', Index.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

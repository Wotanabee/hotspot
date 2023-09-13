from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, musique, listing

urlpatterns = [
    path('', index, name="shazam-index"),
    path('musique-<str:numero_music>/', musique, name="shazam-musique"),
    path('listing/', listing, name="shazam-listing"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
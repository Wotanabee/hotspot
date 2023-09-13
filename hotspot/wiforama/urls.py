
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, listing_image
#from django.conf.urls import handler404

urlpatterns = [
    path('', index, name="wiforama-index"),
    path('listing/', listing_image, name="wiforama-listing"),
] 

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)

#handler404="animanight_hotspot.views.error404"
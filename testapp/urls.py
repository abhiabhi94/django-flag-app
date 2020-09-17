from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('testapp.user_profile.urls')),
    # flag app
    path('flag/', include('flag.urls')),
    # API urls
    path('api/', include('testapp.post.api.urls')),
    path('api/', include('testapp.post.api.urls')),
    path('api/', include('flag.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('testapp.post.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

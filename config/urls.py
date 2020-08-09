from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Home App
    # --------
    # ...
    path("", include("home.urls")),

    # About App
    # --------
    # ...
    path("", include("about.urls")),

    # Authentication
    # --------
    # ...
    path("", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

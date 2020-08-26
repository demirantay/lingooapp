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

    # Profile
    # ---------
    # ...
    path("", include("profile_app.urls")),

    # Profile Settings
    # ---------
    # ...
    path("", include("profile_settings.urls")),

    # Forum
    # ---------
    # ...
    path("", include("forum.urls")),

    # Basic Language Explore
    # ----------
    # ...
    path("", include("basic_language_explore.urls")),

    # Teacher Public About
    # ----------
    # ...
    path("", include("teacher_public_about.urls")),

    # Teacher Authentication
    # -----------
    # ...
    path("", include("teacher_authentication.urls")),

    # Teacher Profile
    path("", include("teacher_profile.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

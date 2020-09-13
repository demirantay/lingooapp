from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path('domingo_private_admin/', admin.site.urls),

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
    # ------------
    # ...
    path("", include("teacher_profile.urls")),

    # Teacher Profile Settings
    # -------------
    # ...
    path("", include("teacher_profile_settings.urls")),

    # Teacher Language Exolore
    # -------------
    # ...
    path("", include("teacher_language_explore.urls")),

    # Teacher Dashboard
    # --------------
    # ...
    path("", include("teacher_dashboard.urls")),

    # Teacher Vocab Container
    # --------------
    # ...
    path("", include("teacher_vocab_container.urls")),

    # Teacher Forum
    # --------------
    # ...
    path("", include("teacher_forum.urls")),

    # Basic Vocab Container
    # --------------
    # ...
    path("", include("basic_vocab_container.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

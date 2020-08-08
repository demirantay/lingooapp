from django.urls import path
from . import views

urlpatterns = [
    # About Us Page
    path('about/', views.about, name="about"),
    # Community Rules
    path("about/communityrules/", views.about_community_rules, name="about_community_rules"),
    # Terms and Agreements
    path("about/terms/", views.about_terms, name="about_terms"),
    # Privacy Policy
    path("about/privacypolicy/", views.about_privacy, name="about_privacy"),
]

# registration/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    # path('stall/', views.stall_registration, name='stall_registration'),
    path('',RedirectView.as_view(pattern_name='register'))
]

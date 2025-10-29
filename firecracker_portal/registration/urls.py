# registration/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('stall/', views.stall_registration, name='stall_registration'),
    path('',RedirectView.as_view(pattern_name='register')),
    path('dc/dashboard/', views.dc_dashboard, name='dc_dashboard'),
    path('dc/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('dc/reject/<int:app_id>/', views.reject_application, name='reject_application'),
    path('unauthorized/', TemplateView.as_view(template_name='unauthorized.html'), name='unauthorized'),
]

# registration/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('stall/', views.stall_registration, name='stall_registration'),
    path('',RedirectView.as_view(pattern_name='register')),
    path('dc/login',views.dc_login, name='dc_login'),
    path('dc/dashboard/', views.dc_dashboard, name='dc_dashboard'),
    path('dc/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('dc/reject/<int:app_id>/', views.reject_application, name='reject_application'),
    path('unauthorized/', TemplateView.as_view(template_name='unauthorized.html'), name='unauthorized'),
    path('hod/login', views.hod_login, name='hod_login'),
    path('hod/dashboard', views.hod_dashboard, name='hod_dashboard'),
    path('process/application/<int:app_id>/', views.process_application, name='process_application'),

]

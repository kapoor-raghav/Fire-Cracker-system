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
     path('hod/dashboard/fresh/', views.hod_fresh_requests, name='hod_fresh_requests'),
    path('hod/dashboard/processed/', views.hod_processed_requests, name='hod_processed_requests'),
    path('process/application/<int:app_id>/', views.process_application, name='process_application'),
    path('forward/application/<int:app_id>/', views.dc_forward_application, name='dc_forward_application'),
    path('dc/dashboard/fresh/', views.dc_fresh_requests, name='dc_fresh_requests'),
    path('dc/dashboard/pending/', views.dc_pending_requests, name='dc_pending_requests'),
    path('dc/dashboard/finalize/', views.dc_finalize_requests, name='dc_finalize_requests'),
]
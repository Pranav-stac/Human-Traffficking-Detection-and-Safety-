from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('report/', views.report_incident, name='report_incident'),
    path('sos/', views.handle_sos, name='handle_sos'),
    # path('upload/', views.receive_files, name='receive_files'),
    path('upload/', views.receive_suspicious_activity, name='receive_suspicious_activity'),
    path('', views.index, name='index'),
    path('admin-grievances/', views.admin_grievances, name='admin-grievances'),
    path('awareness/', views.awareness_page, name='awareness_page'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('community/', views.community, name='community'),
    path('geolocation-tracker/', views.geolocation_tracker, name='geolocation-tracker'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('signup/', views.signup, name='signup'),
    path('grievances/', views.grievances, name='grievances'),
    path('api/incident-reports', views.incident_reports, name='incident-reports'),
    path('victim/', views.victim, name='victim'),
    path('display-images/', views.image_display_view, name='display-images'),
    path('cctv_display/', views.cctv_display, name='cctv_display'),
    path('chat_view/', views.chat_view, name='chat_view'),

    # path('control_monitoring/', views.control_monitoring, name='control_monitoring'),
]
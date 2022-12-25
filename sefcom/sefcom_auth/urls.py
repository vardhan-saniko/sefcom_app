from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vishnu', views.vishnu, name='vishnu'),
    path('auth', views.auth, name='auth'),
    path('authcallback', views.auth_callback, name='auth_callback'),
    path('refreshToken', views.refresh_token, name='refresh_token'),
    path('revokeToken', views.revoke_token, name='revoke_token'),
]
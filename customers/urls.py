from django import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user_page/', edit_profile, name='edit_profile'),
    path('user_page/change_password/', change_password, name='change_password'),
    path('password_reset/', PasswordResetView.as_view(template_name='customers/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='customers/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='customers/password_reset_confirm.html'
    ),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
             template_name='customers/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('profile/<int:pk>', profile, name='profile_page'),
    path('contact/', contact, name='contact'),
]

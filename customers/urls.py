from customers import views

from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user_page/', views.edit_profile, name='edit_profile'),
    path('user_page/change_password/', views.change_password, name='change_password'),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name='customers/password_reset.html'),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='customers/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='customers/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='customers/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path('profile/<int:pk>', views.profile, name='profile_page'),
    path('contact/', views.contact, name='contact'),
]

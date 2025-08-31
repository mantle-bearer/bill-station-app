from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset_password'),
]
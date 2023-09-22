from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView
from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('private_cabinet/<int:pk>', views.private_cabinet, name='private_cabinet'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('wait-confirm-email', views.wait_confirm_email, name='confirm_email'),
    path('confirm_email/<int:pk>', views.ConfirmPage.as_view(), name='confirmed_email'),
    path('password-reset/', views.UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-sent/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    PasswordTokenCheckAPI,
    RegisterView,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    VerifyEmail,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-password-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-password-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]

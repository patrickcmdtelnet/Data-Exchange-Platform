import os

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, serializers, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.renderers import UserRenderer
from accounts.serializers import (
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
)
from utils.utils import Util

User = get_user_model()


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        user = request.data
        password = user.get("password")
        confirm_password = user.get("confirm_password")
        if not password == confirm_password:
            raise serializers.ValidationError("The passwords provided don't match.")
        user.pop("confirm_password")

        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("accounts:email-verify")
        absolute_url = f"http://{current_site}{relative_link}?token={str(token)}"
        email_body = f"Hi, {user.username} use the link below to verify your email. \n{absolute_url}"
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Verification Token",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config], tags=["Auth"])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"email": "Email account successfully verified"},
                status=status.HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get_serializer_class(self):
        return None

    @swagger_auto_schema(tags=["Auth"])
    def get(self, request, uidb64, token):
        redirect_url = request.data.get("redirect_url")
        print(redirect_url)

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(f"{redirect_url}?token_valid=False")
                else:
                    FRONTEND_URL = os.environ.get("FRONTEND_URL", "")
                    return CustomRedirect(f"{FRONTEND_URL}?token_valid=False")

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}"
                )
            else:
                FRONTEND_URL = os.environ.get("FRONTEND_URL", "")
                return CustomRedirect(f"{FRONTEND_URL}?token_valid=False")
        # If token is tampered with
        except DjangoUnicodeDecodeError as e:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(f"{redirect_url}?token_valid=False")
            except UnboundLocalError as er:
                return Response(
                    {"error", "Invalid reset token, please request new reset token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(tags=["Auth"])
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )

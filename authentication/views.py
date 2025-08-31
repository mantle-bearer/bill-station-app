from rest_framework import status, generics, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from .serializers import (
    UserRegistrationSerializer, 
    LoginSerializer, 
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import secrets
import string
from django.core.cache import cache

User = get_user_model()

def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_reset_token():
    """Generate a secure random token"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        tags=["Authentication"],
        summary="Register a new user",
        description="This endpoint registers a new user and returns JWT tokens for authentication.",
        responses={
            201: OpenApiResponse(
                description="User created successfully", 
                response=UserRegistrationSerializer,
                examples=[OpenApiExample(
                    name="User registration successful",
                    value={
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe",
                            "created_at": "2025-04-24T12:00:00Z"
                        }
                    }
                )]
            ),
            400: OpenApiResponse(
                response=UserRegistrationSerializer,
                description="Validation errors",
                examples=[OpenApiExample(
                    name="Invalid email format",
                    value={
                        "status": "failure",
                        "message": "Validation errors",
                        "errors": {
                            "email": ["Enter a valid email address."]
                        }
                    }
                )]
            ),
            409: OpenApiResponse(
                response=UserRegistrationSerializer,
                description="Email already exists",
                examples=[OpenApiExample(
                    name="Email already in use",
                    value={
                        "status": "failure",
                        "message": "Email already exists",
                        "error_code": "email_exists"
                    }
                )]
            ),
            500: OpenApiResponse(
                response=UserRegistrationSerializer,
                description="Internal server error",
                examples=[OpenApiExample(
                    name="Server error",
                    value={
                        "status": "failure",
                        "message": "Internal server error",
                        "error_code": "server_error"
                    }
                )]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        tags=["Authentication"],
        summary="Login user with email and password",
        description="This endpoint allows a user to login and receive JWT tokens for authentication.",
        responses={
            200: OpenApiResponse(
                response=LoginSerializer,
                description="Login successful", 
                examples=[OpenApiExample(
                    name="Login successful",
                    value={
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "user": {
                                "id": 1,
                                "email": "user@example.com",
                                "full_name": "John Doe",
                                "created_at": "2025-04-24T12:00:00Z"
                            },
                            "tokens": {
                                "access": "access_token_value",
                                "refresh": "refresh_token_value"
                            }
                        }
                    }
                )]
            ),
            400: OpenApiResponse(
                response=LoginSerializer,
                description="Invalid credentials",
                examples=[OpenApiExample(
                    name="Invalid credentials",
                    value={
                        "status": "failure",
                        "message": "Invalid credentials",
                        "error_code": "invalid_credentials"
                    }
                )]
            ),
            401: OpenApiResponse(
                response=LoginSerializer,
                description="User account is disabled",
                examples=[OpenApiExample(
                    name="Account disabled",
                    value={
                        "status": "failure",
                        "message": "User account is disabled",
                        "error_code": "account_disabled"
                    }
                )]
            ),
            500: OpenApiResponse(
                response=LoginSerializer,
                description="Internal server error",
                examples=[OpenApiExample(
                    name="Server error",
                    value={
                        "status": "failure",
                        "message": "Internal server error",
                        "error_code": "server_error"
                    }
                )]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        tags=["Authentication"],
        summary="Request password reset token",
        description="This endpoint generates a password reset token and sends it to the user.",
        responses={
            200: OpenApiResponse(
                response=ForgotPasswordSerializer,
                description="Reset token generated",
                examples=[OpenApiExample(
                    name="Password reset token generated",
                    value={
                        "status": "success",
                        "message": "Password reset token generated",
                        "reset_token": "reset_token_value",
                        "expires_in": "10 minutes"
                    }
                )]
            ),
            404: OpenApiResponse(
                response=ForgotPasswordSerializer,
                description="User not found",
                examples=[OpenApiExample(
                    name="User not found",
                    value={
                        "status": "failure",
                        "message": "User with this email does not exist",
                        "error_code": "user_not_found"
                    }
                )]
            ),
            400: OpenApiResponse(
                response=ForgotPasswordSerializer,
                description="Bad request",
                examples=[OpenApiExample(
                    name="Invalid email format",
                    value={
                        "status": "failure",
                        "message": "Invalid email format",
                        "error_code": "invalid_email"
                    }
                )]
            ),
            500: OpenApiResponse(
                response=ForgotPasswordSerializer,
                description="Internal server error",
                examples=[OpenApiExample(
                    name="Server error",
                    value={
                        "status": "failure",
                        "message": "Internal server error",
                        "error_code": "server_error"
                    }
                )]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                reset_token = generate_reset_token()
                cache_key = f"password_reset:{reset_token}"
                cache.set(cache_key, user.id, timeout=600)
                return Response({
                    'message': 'Password reset token generated',
                    'reset_token': reset_token,
                    'expires_in': '10 minutes'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'error': 'User with this email does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        tags=["Authentication"],
        summary="Reset password using token",
        description="This endpoint allows a user to reset their password using the reset token.",
        responses={
            200: OpenApiResponse(
                response=ResetPasswordSerializer,
                description="Password reset successful",
                examples=[OpenApiExample(
                    name="Password reset successful",
                    value={
                        "status": "success",
                        "message": "Password reset successful"
                    }
                )]
            ),
            400: OpenApiResponse(
                response=ResetPasswordSerializer,
                description="Invalid or expired token",
                examples=[OpenApiExample(
                    name="Invalid or expired reset token",
                    value={
                        "status": "failure",
                        "message": "Invalid or expired reset token",
                        "error_code": "invalid_token"
                    }
                )]
            ),
            404: OpenApiResponse(
                response=ResetPasswordSerializer,
                description="User not found",
                examples=[OpenApiExample(
                    name="User not found",
                    value={
                        "status": "failure",
                        "message": "User not found",
                        "error_code": "user_not_found"
                    }
                )]
            ),
            500: OpenApiResponse(
                response=ResetPasswordSerializer,
                description="Internal server error",
                examples=[OpenApiExample(
                    name="Server error",
                    value={
                        "status": "failure",
                        "message": "Internal server error",
                        "error_code": "server_error"
                    }
                )]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            cache_key = f"password_reset:{token}"
            user_id = cache.get(cache_key)
            
            if user_id is None:
                return Response({
                    'error': 'Invalid or expired reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                cache.delete(cache_key)
                return Response({
                    'message': 'Password reset successful'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


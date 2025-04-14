from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .serializers import (
    UserRegistrationSerializer, UserDetailSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, RequestCodeSerializer, ResetPasswordSerializer,
    ActivateAccountSerializer, LoginSerializer
)
from . import services

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'request_code', 'reset_password']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'activate':
            return ActivateAccountSerializer
        if self.action == 'login':
            return LoginSerializer
        elif self.action == 'me':
            return UserDetailSerializer
        elif self.action == 'update_name':
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'request_code':
            return RequestCodeSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        return UserDetailSerializer

    @action(detail=False, methods=['post'], url_path='activate')
    def activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'], code=serializer.validated_data['code'])
        except User.DoesNotExist:
            return Response({'detail': 'Invalid email or code'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.code = None
        user.save()
        return Response({'detail': 'Account activated!'})

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='update-name')
    def update_name(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password updated'})

    @action(detail=False, methods=['post'], url_path='request-code')
    def request_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            user.save()
            data = {
                "email_body": f"Your code: {user.code}",
                "to_email": user.email
            }
            services.send_mail(data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Code sent to email'})

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'], code=serializer.validated_data['code'])
        except User.DoesNotExist:
            return Response({'detail': 'Invalid code or email'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.code = None
        user.save()

        return Response({'detail': 'Password reset'})

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request):
        user = request.user
        user.delete()
        return Response({'detail': 'Account deleted'})

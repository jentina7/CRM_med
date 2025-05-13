from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from system_app.models import UserProfile, Specialty


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail: Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user=serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh токен отсутствует."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Ошибка обработки токена."}, status=status.HTTP_400_BAD_REQUEST)


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(role='doctor')
    serializer_class = DoctorProfileSerializer


class ReceptionProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(role='reception')
    serializer_class = ReceptionProfileSerializer


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(role='admin')
    serializer_class = AdminProfileSerializer





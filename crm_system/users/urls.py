from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

router = DefaultRouter()
router.register(r'specialties', SpecialtyViewSet, basename='specialties')
router.register(r'doctors', DoctorProfileViewSet, basename='doctor_profile')
router.register(r'receptions', ReceptionProfileViewSet, basename='reception_profile')
router.register(r'admins', AdminProfileViewSet, basename='admin_profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register_reception'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

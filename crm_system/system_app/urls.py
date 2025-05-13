from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import (DepartmentViewSet, RecordingTimeViewSet, ServiceListAPIView, ServiceCreateAPIView,
                    PatientCreateAPIView, PatientRetrieveUpdateDestroyAPIView, PatientDataAPIView, PatientDataForDoctorViewSet)


router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename='department-list')
router.register(r'recording_time', RecordingTimeViewSet, basename='recording_time-list')
router.register(r'patient_data_for_doctor', PatientDataForDoctorViewSet, basename='patient_data_for_doctor-list')


urlpatterns = [
    path('', include(router.urls)),

    path("service/", ServiceListAPIView.as_view(), name="service_list"),
    path("service/create/", ServiceCreateAPIView.as_view(), name="service_create"),

    path("patient/create/", PatientCreateAPIView.as_view(), name="patient_create"),
    path("patient/<int:pk>/", PatientRetrieveUpdateDestroyAPIView.as_view(), name="patient_update"),
    path("patient_data/", PatientDataAPIView.as_view(), name="patient_data"),
    # path("patient_data_for_doctor/", PatientDataForDoctorUpdateAPIView.as_view(), name="patient_data_for_doctor"),
]
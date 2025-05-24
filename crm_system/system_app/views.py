from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import (DepartmentSerializer, ServiceListSerializer, ServiceCreateSerializer, RecordingTimeSerializer,
                          PatientCreateSerializer, PatientUpdateSerializer, PatientDataSerializer, PatientDataForDoctorSerializer,
                          HistoryRecordingSerializer, AdmissionHistorySerializer)
from .models import Department, Service, RecordingTime, Patient, HistoryRecording


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer


class ServiceCreateAPIView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceCreateSerializer


class RecordingTimeViewSet(viewsets.ModelViewSet):
    queryset = RecordingTime.objects.all()
    serializer_class = RecordingTimeSerializer


class PatientCreateAPIView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer


class PatientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientUpdateSerializer


class PatientDataAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDataSerializer


class PatientDataForDoctorViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientDataForDoctorSerializer


class HistoryRecordingViewSet(viewsets.ModelViewSet):
    queryset = HistoryRecording.objects.all()
    serializer_class = HistoryRecordingSerializer


class AdmissionHistoryViewSet(viewsets.ModelViewSet):
    queryset = HistoryRecording.objects.filter(status="был в приеме")
    serializer_class = AdmissionHistorySerializer

    # def get_queryset(self):
    #     status_param = self.request.query_params.get('status')
    #     queryset = HistoryRecording.objects.all()
    #     if status_param == "был в приеме":
    #         queryset = queryset.filter(status="был в приеме")
    #     return queryset


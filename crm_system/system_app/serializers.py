from rest_framework import serializers
from .models import Department, Service, RecordingTime, Patient
from users.serializers import DoctorProfileForDepartSerializer


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["service_name", "service_price", "department"]


class DepartmentSerializer(serializers.ModelSerializer):
    service_depart = ServiceCreateSerializer(many=True, read_only=True)
    doctor = DoctorProfileForDepartSerializer()
    class Meta:
        model = Department
        fields = ["department_name", "doctor", "floor", "cabinet", "service_depart"]


class DepartmentForServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department_name", "floor", "cabinet"]  # убрать floor and cabinet


class ServiceListSerializer(serializers.ModelSerializer):
    department = DepartmentForServiceSerializer(read_only=True)
    class Meta:
        model = Service
        fields = ["service_name", "service_price", "department"]


class RecordingTimeSerializer(serializers.ModelSerializer):
    shift_start = serializers.TimeField(format="%H:%M")
    shift_end = serializers.TimeField(format="%H:%M")
    class Meta:
        model = RecordingTime
        fields = ["shift_start", "shift_end"]


class PatientCreateSerializer(serializers.ModelSerializer):
    recording_time = serializers.PrimaryKeyRelatedField(many=True, queryset=RecordingTime.objects.all())
    # reception =
    # doctor = DoctorProfileForDepartSerializer()
    class Meta:
        model = Patient
        fields = ["full_name", "birthday", "gender", "phone_number", "department", "service",
                  "recording_time", "doctor", "type_record", "reception", "created_date"]
# added doctor, reception


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["department", "service", "recording_time", "type_record", "created_date"]


class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["full_name", "gender", "phone_number"]


# class PatientCreateForDoctorSerializer(serializers.ModelSerializer):
#     recording_time = RecordingTimeSerializer()
#     class Meta:
#         model = Patient
#         fields = ["service", "medical_history", "full_name", "phone_number", "recording_time", "gender",
#                   "type_record", "created_date"]


class PatientDataForDoctorSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y " "%H:%M")
    class Meta:
        model = Patient
        fields = ["full_name", "gender", "phone_number", "medical_history", "created_date"]
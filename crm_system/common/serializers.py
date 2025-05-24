from rest_framework import serializers
from system_app.models import UserProfile, Department, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']


class DepartmentForServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department_name", "floor", "cabinet"]


class DoctorProfileForDepartSerializer(serializers.ModelSerializer):
    department = DepartmentForServiceSerializer()
    specialty = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['fio', 'profile_picture', 'age', 'phone_number',
                  'specialty', 'experience', 'department', 'created_date']

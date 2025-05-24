from rest_framework import serializers
from system_app.models import  UserProfile, Department
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from common.serializers import DepartmentForServiceSerializer, SpecialtySerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio', 'age', 'username', 'profile_picture', 'email', 'password',
                  'phone_number', 'experience', 'specialty', 'bonus_doctor', 'role', 'created_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        specialties_data = validated_data.pop('specialty')

        user = UserProfile.objects.create_user(**validated_data)

        user.specialty.set(specialties_data)

        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Invalid or already revoked token'})


# class SpecialtySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Specialty
#         fields = ['specialty_name']


class DoctorProfileSerializer(serializers.ModelSerializer):
    department = DepartmentForServiceSerializer()
    specialty = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['fio', 'username', 'profile_picture', 'age', 'role', 'phone_number',
                  'specialty', 'experience', 'department', 'bonus_doctor', 'created_date']


# class DoctorProfileForDepartSerializer(serializers.ModelSerializer):
#     department = DepartmentForServiceSerializer()
#     specialty = SpecialtySerializer(many=True, read_only=True)
#
#     class Meta:
#         model = UserProfile
#         fields = ['fio', 'profile_picture', 'age', 'phone_number',
#                   'specialty', 'experience', 'department', 'created_date']


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'fio', 'profile_picture', 'role', 'experience', 'specialty', 'department', 'bonus_doctor',
                  'phone_number', 'email']


class DoctorListSerializer(serializers.ModelSerializer):
    department = DepartmentForServiceSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'fio', 'department', 'phone_number']


class DoctorDetailSerializer(serializers.ModelSerializer):
    department = DepartmentForServiceSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True,
        source='department'
    )
    specialty = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['fio', 'profile_picture', 'role', 'experience', 'specialty', 'department', 'bonus_doctor',
                  'phone_number', 'email', 'department_id']


class DoctorNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio']


class ReceptionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio', 'email', 'role', 'phone_number']


class ReceptionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fio','username', 'profile_picture', 'age', 'role', 'phone_number', 'created_date']





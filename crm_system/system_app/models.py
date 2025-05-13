from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.specialty_name}'


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'doctor'),
        ('reception', 'reception'),
        ('admin', 'admin')
    )
    fio = models.CharField(max_length=256)
    role = models.CharField(max_length=64, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(null=True, blank=True, region='KG', unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(18),
        MaxValueValidator(110)
    ], null=True, blank=True)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(70)], null=True, blank=True)
    specialty = models.ManyToManyField(Specialty, related_name='specialty_doctor')
    bonus_doctor = models.PositiveSmallIntegerField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.fio} -- {self.role}'


class Department(models.Model):
    department_name = models.CharField(max_length=50, unique=True)
    floor = models.PositiveIntegerField(default=1)
    cabinet = models.PositiveSmallIntegerField(default=0)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="depart_doctor")

    def __str__(self):
        return f"{self.department_name} - {self.cabinet}"


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_price = models.PositiveIntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="service_depart")
    # discount

    def __str__(self):
        return f"{self.service_name} - {self.service_price}"


class RecordingTime(models.Model):
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return f"{self.shift_start} - {self.shift_end}"


class Patient(models.Model):
    full_name = models.CharField(max_length=100)
    birthday = models.DateField()
    GENDER_CHOICES =(
        ('man', 'man'),
        ('woman', 'woman')
    )
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="patient_depart")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="patient_service")
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="patient_doctor")
    reception = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="patient_reception")
    recording_time = models.ManyToManyField(RecordingTime)
    TYPE_CHOICES = (
        ('online', 'онлайн запись'),
        ('queue', 'живая очередь'),
        ('cencel', 'отмена')
    )
    type_record = models.CharField(max_length=32, choices=TYPE_CHOICES, default='queue')
    medical_history = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.recording_time} - {self.type_record}"
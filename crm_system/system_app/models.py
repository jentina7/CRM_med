from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.specialty_name}'


class Department(models.Model):
    department_name = models.CharField(max_length=50, unique=True)
    floor = models.PositiveIntegerField(default=1)
    cabinet = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return f"{self.department_name} - {self.cabinet}"


class UserProfile(AbstractUser):
    username = models.CharField(null=True, blank=True)
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
    specialty = models.ManyToManyField(Specialty, related_name='specialty_doctor', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='depart_doctor', null=True, blank=True)
    bonus_doctor = models.PositiveSmallIntegerField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.fio} -- {self.role}'


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


class HistoryRecording(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_history')
    STATUS_CHOICES = (
        ("был в приеме", "был в приеме"),
        ("в ожидании", "в ожидании"),
        ("отменен", "отменен")
    )
    status = models.CharField(max_length=24, choices=STATUS_CHOICES)

    @classmethod
    def get_count_total_status(cls):
        data = cls.objects.values('status').annotate(count=Count('status'))
        status_count = {item["status"]: item['count'] for item in data}
        total_sum = sum(status_count.values())
        status_count['total_sum'] = total_sum
        return status_count

    @classmethod
    def reception_status(cls):
        total = cls.objects.filter(status="был в приеме").count()
        return {
            "status": "был в приеме",
            "total_sum": total
        }

    @classmethod
    def get_count_statuses(cls):
        data = cls.objects.values('status').annotate(count=Count('status'))
        status_count = {item["status"]: item['count'] for item in data}
        return status_count

    def __str__(self):
        return f'{self.patient}, {self.status}'



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")

        user = UserProfile(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

        user = self.create_user(email=email, password=password, **extra_fields)

        return user
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE_CHOICES = (
    ('doctor', 'doctor'),
    ('reception', 'reception'),
    ('superuser', 'superuser')
)

class UserProfile(AbstractUser):
    role = models.CharField(max_length=64, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.specialty_name}'


class Doctor(UserProfile):
    phone_number = PhoneNumberField(null=True, blank=True, region='KG', unique=True)
    profile_picture = models.ImageField(upload_to='profiles/')
    age = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(18),
        MaxValueValidator(110)
    ], null=True, blank=True)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(50)])
    specialty = models.ManyToManyField(Specialty, related_name='specialty_doctor')

    def __str__(self):
        specialties = ', '.join([s.specialty_name for s in self.specialty.all()])
        return f'{self.first_name} {self.last_name} -- {self.role} -- {specialties or "No Specialty"}'

    class Meta:
        verbose_name_plural = "Doctor"


class Reception(UserProfile):
    phone_number = PhoneNumberField(null=True, blank=True, region='KG', unique=True)

    class Meta:
        verbose_name_plural = "Reception"

    def __str__(self):
        return f'{self.first_name} {self.last_name}, -- {self.role}'


class SuperUser(UserProfile):
    pass

    class Meta:
        verbose_name_plural = "SuperUser"


class Service(models.Model):
    service_name = models.CharField(max_length=128)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(1000000)])
    is_has_service = models.BooleanField()
    count = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def get_discount_price(self):
        discount_rate = self.discount / 100
        discount_price = self.price * (1 - discount_rate)
        return round(discount_price, 2)

    def __str__(self):
        return f'{self.service_name} {self.price}, -- {self.discount}'


class Patient(models.Model):
    fio = models.CharField(max_length=100)
    GENDER_CHOICES =(
        ('man', 'man'),
        ('woman', 'woman')
    )
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(auto_now=True)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    dop_phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    inn = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message="ИНН должен состоять ровно из 14 цифр."
            )
        ]
    )
    password = models.CharField(max_length=100)
    BLOOD_CHOICES = (
        ('I+', 'I+'),
        ('I-', 'I-'),
        ('II+', 'II+'),
        ('II-', 'II-'),
        ('III+', 'III+'),
        ('III-', 'III-'),
        ('IV+', 'IV+'),
        ('IV-', 'IV-'),
    )
    blood_type = models.CharField(max_length=8, choices=BLOOD_CHOICES)

    def __str__(self):
        return f"{self.fio} - {self.inn}"


class Department(models.Model):
    department_name = models.CharField(max_length=64, unique=True)
    floor = models.SmallIntegerField(default=1)
    cabinet = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.department_name} - {self.floor} -{self.cabinet}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    comment = models.TextField()
    QUEUE_CHOICES = (
        ("queue", "живая очередь"),
        ("call", "звонок"),
    )
    queue_status = models.CharField(max_length=16, choices=QUEUE_CHOICES, default="queue")
    vaccination = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ("запланировано", "запланировано"),
        ("завершено", "завершено"),
        ("отменено", "отменено"),

    )
    status_appointment = models.CharField(max_length=16, choices=STATUS_CHOICES)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.patient} - {self.status_appointment}"



class HistoryAppointment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.status}"



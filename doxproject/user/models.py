
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.fields import DateField, PositiveIntegerField

# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = (
        ("M", "Male"),

        ("F", "Female"),
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False, null=False)
    address = models.CharField(max_length=300)
    cart = models.ExpressionList
    role = models.CharField()
    id_number = models.PositiveIntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES)

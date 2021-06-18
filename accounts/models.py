from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   phonenumber = models.CharField(verbose_name="Телефон", max_length=10)
   birthdate = models.DateField(verbose_name="Дата рождения")


class Emailcode(models.Model):
   email = models.CharField(max_length=200)
   code = models.CharField(max_length=5)
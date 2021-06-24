from django.conf import settings
from django.db import models
from django.utils import timezone


class Item(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    sec_category = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    info = models.TextField()
    img_count = models.DecimalField(max_digits=5, decimal_places=2)
    lamoda_id = models.CharField(max_length=20)


class Images(models.Model):
    count = models.DecimalField(max_digits=5, decimal_places=0)
    image = models.FileField(upload_to='media/')
    is_active = models.IntegerField()





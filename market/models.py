from django.conf import settings
from django.db import models
from django.utils import timezone


class Item(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    sec_category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    info = models.TextField()
    image1 = models.ImageField(null=True, blank=True, upload_to="images")
    image2 = models.ImageField(null=True, blank=True, upload_to="images")
    image3 = models.ImageField(null=True, blank=True, upload_to="images")


    def publish(self):
        self.published_date = timezone.now()
        self.save()



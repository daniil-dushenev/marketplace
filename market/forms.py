from django import forms
from .models import Item, Images
from django.db import models


class CreateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['brand', 'name', 'color', 'category', 'sec_category', 'price', 'info']


class ImageForm(forms.ModelForm):
    image = models.FileField()
    class Meta:
        model = Images
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs=
                                         {'class': 'form-control',
                                          'multiple': ''}
                                         )}
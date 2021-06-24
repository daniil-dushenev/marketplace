from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Emailcode
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['birthdate', 'phonenumber']
        widgets = {
            'birthdate': forms.DateInput(format=('%Y-%d-%m'),
                    attrs={'class': 'form-control'}
                    )}


class CodeForm(forms.ModelForm):

    class Meta:
        model = Emailcode
        fields = ['code']


class AccountForm(forms.ModelForm):
    user_id = 0

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
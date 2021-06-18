from .forms import UserForm
from .forms import ProfileForm
from .forms import CodeForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Emailcode


def generate_code():
    random.seed()
    return str(random.randint(10000,99999))


def register(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            if str(User.objects.filter(email=u_form.cleaned_data.get('email'))) != '<QuerySet []>':
                print('Ошибка! Пользователь с такой почтой уже есть')
                return redirect(register)
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            profile = User.objects.get(email=user.email)
            profile.is_active = False
            profile.save()
            code = generate_code()
            message = 'Ваш код подтверждения: ' + str(code) + '. Никому его не сообщайте!'
            Emailcode.objects.create(email=user.email, code=code)
            send_mail('Код подтверждения', message,
                      settings.EMAIL_HOST_USER,
                      [user.email],
                      fail_silently=False)
            return redirect(endreg)

    else:
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

    return render(request, 'signup.html', {'u_form': u_form, 'p_form': p_form})


def endreg(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get("code")
            if str(Emailcode.objects.filter(code=code_use)) != '<QuerySet []>':
                profile = Emailcode.objects.get(code=code_use)
                user = User.objects.get(email=profile.email)
                user.is_active = True
                user.save()
                message = 'Здравствуйте, ' + str(user.first_name) + '! Ваш аккаунт успешно зарегистрирован.'
                send_mail('Код подтверждения', message,
                          settings.EMAIL_HOST_USER,
                          [user.email],
                          fail_silently=False)
                return redirect('login')
            else:
                form.add_error(None, "Код подтверждения не совпадает.")
                return redirect(endreg)
        else:
            form.add_error(None, '1Unknown or disabled account')
            return render(request, 'endreg.html', {'form': form})
    else:
        form = CodeForm(request.POST)

    return render(request, 'endreg.html', {'form': form})
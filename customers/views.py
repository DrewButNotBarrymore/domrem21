from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import RequestContext

from ads.models import Ads
from customers.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm, ProfileUpdateForm, \
    ContactForm, MyPasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash

from customers.models import CustomUser, Profile


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрированы! Заполните, пожалуйста, профиль.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = CustomUserCreationForm()
    return render(request, 'customers/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserLoginForm()
    return render(request, 'customers/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def profile(request, pk):
    profile_item = get_object_or_404(CustomUser, pk=pk)
    ads_list = Ads.objects.filter(author=profile_item)

    data = {
        'ads_list': ads_list,
        'profile_item': profile_item,
    }

    return render(request, 'customers/profile.html', data)


@login_required
def edit_profile(request):
    ads_list = Ads.objects.filter(author=request.user)

    if request.method == "POST":
        update_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        update_user = CustomUserUpdateForm(request.POST, instance=request.user)

        if update_user.is_valid() and update_profile.is_valid():
            update_user.save()
            update_profile.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен')
            return redirect('edit_profile')
    else:
        update_profile = ProfileUpdateForm(instance=request.user.profile)
        update_user = CustomUserUpdateForm(instance=request.user)

    data = {
        'update_profile': update_profile,
        'update_user': update_user,
        'ads_list': ads_list,
    }

    return render(request, 'customers/user_page.html', data)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                             'domrem21@mail.ru', ['undrew.ivanov@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, f'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, f'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка валидации!')
    else:
        form = ContactForm()
    return render(request, 'customers/contact_form.html', {"form": form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)
    return render(request, 'customers/change_password.html', {
        'form': form
    })

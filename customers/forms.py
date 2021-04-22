from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django import forms
from captcha.fields import CaptchaField

from .models import CustomUser, Profile


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail',
                                widget=forms.EmailInput(attrs={'class': "form-control form-control-grey"}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"}))


class CustomUserCreationForm(UserCreationForm):
    CHOICES = (
        ('IM', 'Частный мастер'),
        ('CO', 'Компания'),
    )
    type = forms.ChoiceField(label='Тип пользователя',
                             widget=forms.Select(attrs={'class': "form-select form-control-grey"}), choices=CHOICES)
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': "form-control form-control-grey"}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('type', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': "form-control form-control-grey"}))

    class Meta:
        model = CustomUser
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-grey"}))
    photo = forms.ImageField(required=False,
                             widget=forms.ClearableFileInput())
    contact_person = forms.CharField(required=False,
                                     widget=forms.TextInput(attrs={"class": "form-control form-control-grey"}))
    about = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={"class": "form-control form-control-grey", "rows": 5}))

    class Meta:
        model = Profile
        fields = ['name', 'photo', 'contact_person', 'about']


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', max_length=150,
                              widget=forms.TextInput(attrs={"class": "form-control form-control-grey"}))
    content = forms.CharField(label='Текст', max_length=500,
                              widget=forms.Textarea(attrs={"class": "form-control form-control-grey", "rows": 5}))
    captcha = CaptchaField(label='Капча')


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"})
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"})
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-grey"})
    )

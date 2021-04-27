from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    CHOICES = (
        ('IM', 'Частный мастер'),
        ('CO', 'Компания'),
    )
    type = models.CharField(
        max_length=15, choices=CHOICES, default='IM', verbose_name='Тип пользователя'
    )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        default=False, verbose_name='Внутренний пользователь'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата регистрации'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse('profile_page', kwargs={'pk': self.id})

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    name = models.CharField(max_length=100, verbose_name='Имя/название', blank=True)
    about = models.TextField(blank=True, verbose_name='О пользователе')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/', verbose_name='Изображение профиля', blank=True
    )
    contact_person = models.CharField(
        max_length=50, verbose_name='Контактное лицо', blank=True
    )

    def __str__(self):
        return f'Профайл пользователя {self.user.email}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.photo:
            image = Image.open(self.photo.path)

            if image.height > 500 or image.width > 500:
                resize = (500, 500)
                image.thumbnail(resize)
                image.save(self.photo.path)

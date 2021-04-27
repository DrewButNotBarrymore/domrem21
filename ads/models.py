from customers.models import CustomUser

from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name='Наменование категории'
    )
    keys = models.CharField(max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Ads(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, verbose_name='Автор'
    )
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категория'
    )
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Текст объявления')
    phone = models.TextField(blank=True, max_length=20, verbose_name='Телефон')
    price = models.TextField(blank=True, max_length=15, verbose_name='Стоимость')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def get_absolute_url(self):
        return reverse('ad_page', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Images(models.Model):
    ad = models.ForeignKey(
        Ads,
        blank=True,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Объявление',
    )
    img = models.ImageField(
        upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True
    )

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.ad.title

    def get_absolute_url(self):
        return reverse('ad_page', kwargs={'pk': self.pk})

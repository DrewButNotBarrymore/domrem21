from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_photo', 'ad', 'img', )
    list_display_links = ('id', 'ad')
    search_fields = ('id', 'ad__title',)

    def get_photo(self, obj):
        if obj.img:
            return mark_safe(f'<img src ="{obj.img.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


class AdsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'category', 'author', 'is_published',)
    list_filter = ('category__title',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()

    list_editable = ('is_published',)
    search_fields = ('title', 'category__title')
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('-updated_at',)


admin.site.register(Ads, AdsAdmin)
admin.site.register(Category)
admin.site.register(Images, ImagesAdmin)

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'type', 'date_joined', 'is_staff', 'is_active',)
    list_filter = ('type', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'type', 'password', 'date_joined')}),
        ('Роли', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'type', 'password1', 'password2', 'is_staff', 'is_active')}),
    )
    list_editable = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('date_joined',)
    ordering = ('email', '-date_joined')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'contact_person', 'about', 'get_photo', 'photo',)
    list_display_links = ('id', 'name',)
    list_filter = ('user',)
    search_fields = ('name', 'user__email',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src ="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.photo:
            return self.readonly_fields
        return ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(Group)

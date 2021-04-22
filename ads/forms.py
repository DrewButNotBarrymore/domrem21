from ckeditor.widgets import CKEditorWidget
from django import forms

from ads.models import Ads


class AdForm(forms.ModelForm):
    photos = forms.ImageField(label='Загрузите примеры ваших работ',
                              widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    content = forms.CharField(label='Текст объявления', widget=CKEditorWidget())

    class Meta:
        model = Ads
        fields = ['title', 'category', 'content', 'phone', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-grey'}),
            'category': forms.Select(attrs={'class': 'form-select form-control-grey'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-grey'}),
            'price': forms.TextInput(attrs={'class': 'form-control form-control-grey'}),
        }

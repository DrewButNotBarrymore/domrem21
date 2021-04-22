from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeAds.as_view(), name='home'),
    path('master_ads/', MasterAds.as_view(), name='master_ads'),
    path('company_ads/', CompanyAds.as_view(), name='company_ads'),
    path('category/<int:category_id>/', AdsByCategory.as_view(), name='category'),
    path('ad_page/<int:pk>', DetailAd.as_view(), name='ad_page'),
    path('add_ad/', add_ad, name='add_ad'),
    path('search/', Search.as_view(), name='search'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('edit_ad/<int:pk>', edit_ad, name='edit_ad'),
    path('remove_ad/<int:pk>', remove_ad, name='remove_ad'),
    path('remove_img/<int:pk>', remove_img, name='remove_img'),
    path('master_info/', master_info, name='master_info'),
    path('company_info/', company_info, name='company_info'),
    path('about/', about, name='about'),
]

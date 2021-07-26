from ads import views

from django.urls import path

urlpatterns = [
    path('', views.HomeAds.as_view(), name='home'),
    path('master_ads/', views.MasterAds.as_view(), name='master_ads'),
    path('company_ads/', views.CompanyAds.as_view(), name='company_ads'),
    path('category/<int:category_id>/', views.AdsByCategory.as_view(), name='category'),
    path('ad_page/<int:pk>', views.DetailAd.as_view(), name='ad_page'),
    path('add_ad/', views.add_ad, name='add_ad'),
    path('search/', views.Search.as_view(), name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('edit_ad/<int:pk>', views.edit_ad, name='edit_ad'),
    path('remove_ad/<int:pk>', views.remove_ad, name='remove_ad'),
    path('remove_img/<int:pk>', views.remove_img, name='remove_img'),
]

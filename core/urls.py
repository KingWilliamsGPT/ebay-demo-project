from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.SearchPage.as_view(), name='search'),
    path('product/<int:product_id>/', views.ProductView.as_view(), name='detail'),
]

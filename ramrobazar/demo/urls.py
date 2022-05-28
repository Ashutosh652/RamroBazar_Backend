from django.urls import path
from . import views


app_name = 'demo'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
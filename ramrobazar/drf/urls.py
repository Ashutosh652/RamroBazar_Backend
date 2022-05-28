from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ramrobazar.drf import views


app_name = 'drf'

router = DefaultRouter()
router.register(r'products', views.AllProductsViewSet, basename='allproducts')
# router.register(r'productinventory', views.ProductInventoryViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
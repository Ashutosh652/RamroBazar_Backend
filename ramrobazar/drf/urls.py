from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ramrobazar.drf import views


app_name = 'drf'

router = DefaultRouter()
router.register(r'productsandservices', views.ProductsOrServicesList, basename='productsandservices')
router.register(r'user/register', views.UserRegister, basename='user-register')

urlpatterns = [
    path('', include(router.urls)),
    # path('user/register', views.UserRegister.as_view(), name='user-register'),
]
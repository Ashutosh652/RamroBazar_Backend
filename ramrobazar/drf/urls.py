from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    )
from ramrobazar.drf import views


app_name = 'drf'

router = DefaultRouter()
router.register(r'items', views.ItemList, basename='items')
router.register(r'item/add', views.AddItem, basename='item-add')
router.register(r'item/update', views.UpdateItem, basename='item-update')
router.register(r'media/add', views.AddMedia, basename='media-add')
router.register(r'categories', views.CategoryList, basename='categories')
router.register(r'user/register', views.UserRegister, basename='user-register')
router.register(r'user/logout', views.BlackListToken, basename='user-logout')
router.register(r'users', views.UserList, basename='users')
router.register(r'user/update', views.UserUpdate, basename='user-update')
router.register(r'user/update-password', views.UserPasswordUpdate, basename='user-update-password')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
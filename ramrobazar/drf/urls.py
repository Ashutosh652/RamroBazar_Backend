from email.mime import base
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from ramrobazar.drf import views


app_name = "drf"

router = DefaultRouter()
router.register(r"brands", views.BrandList, basename="brands")
router.register(r"items", views.ItemList, basename="items")
# router.register(r"<str:slug>/comment", views.CommentDetail, basename="comments")
router.register(r"item/add", views.AddItem, basename="item-add")
router.register(
    r"item/specification/add",
    views.AddItemSpecification,
    basename="item-specification-add",
)
router.register(
    r"item/specification/remove",
    views.RemoveItemSpecification,
    basename="item-specification-remove",
)
router.register(r"item/update", views.UpdateItem, basename="item-update")
router.register(r"media/add", views.AddMedia, basename="media-add")
router.register(r"categories", views.CategoryList, basename="categories")
router.register(r"user/register", views.UserRegister, basename="user-register")
# router.register(r'user/logout', views.BlackListToken, basename='user-logout')
router.register(r"users", views.UserList, basename="users")
router.register(r"user/update", views.UserUpdate, basename="user-update")
router.register(
    r"user/update-password", views.UserPasswordUpdate, basename="user-update-password"
)
router.register(r"user/wishlist", views.GetWishList, basename="wishlist")
router.register(r"comment/add", views.AddComment, basename="comment-add")
router.register(r"comment/update", views.UpdateComment, basename="comment-update")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path('user/logout/', views.BlackListToken.as_view(), name='user-logout'),
]

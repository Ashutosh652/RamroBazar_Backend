from crypt import methods
from functools import partial
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ramrobazar.account.models import User
from ramrobazar.inventory.models import (
    Brand,
    Category,
    Item,
    Comment,
    ItemSpecification,
)
from ramrobazar.drf.serializers import (
    BrandSerializer,
    ItemSpecificationSerializer,
    MediaSerializer,
    RegisterUserSerializer,
    MyTokenObtainPairSerializer,
    ItemSerializer,
    ItemDetailSerializer,
    AddItemSerializer,
    CategorySerializer,
    UserSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CommentSerializer,
)
from ramrobazar.drf.permissions import CustomProfileUpdatePermission


"""..........................Customizing Token Claims..................................................................."""


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""..........................Customizing Token Claims End..................................................................."""


class MainView(View):
    """View for listing the endpoints."""

    def get(self, request, *args, **kwargs):
        return render(request, "drf/main.django-html")


class BrandList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing all brands"""

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


class CategoryList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing all categories."""

    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ItemList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing and retrieving all items for sale."""

    # items_for_sale = [item.id for item in Item.objects.all() if item.sold_status.is_sold == False]
    # queryset = Item.objects.filter(pk__in=items_for_sale)
    queryset = Item.objects.filter(is_visible=True, is_sold=False)
    queryset_actions = {"retrieve": Item.objects.all()}
    serializer_class = ItemSerializer
    serializer_action_classes = {
        "retrieve": ItemDetailSerializer,
    }
    permission_classes = [AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "category__slug",
        "brand__name",
    ]
    search_fields = ["name", "description", "category__name", "brand__name", "location"]

    def get_queryset(self):
        try:
            return self.queryset_actions[self.action]
        except:
            return self.queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except:
            return self.serializer_class

    def retrieve(self, request, slug=None):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def comments(self, request, slug=None):
        item = Item.objects.get(slug=slug)
        queryset = Comment.objects.filter(item=item)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def wishlist_add(self, request, slug=None):
        item = Item.objects.get(slug=slug)
        user = request.user
        item.users_wishlist.add(user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def wishlist_remove(self, request, slug=None):
        item = Item.objects.get(slug=slug)
        user = request.user
        item.users_wishlist.remove(user)
        return Response(status=status.HTTP_200_OK)


class GetWishList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for getting wishlist of users."""

    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Item.objects.filter(users_wishlist=self.request.user.id)


class AddItem(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for adding products by users."""

    serializer_class = AddItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """Try to get the brand with the id that was sent if it exists. Otherwise send an error response."""
        try:
            brand_id = request.data["brand"]
            if brand_id == None:
                brand = None
            else:
                brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response(
                {"detail": "brand does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        """Try to get the category with the ids that was sent if they exist. Send an error response if at least one doesn't exist."""
        category = []
        try:
            for cat in request.data["category"]:
                category.append(Category.objects.get(id=cat))
        except Category.DoesNotExist:
            return Response(
                {"detail": "at least one category does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer, brand, category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, brand, category):
        serializer.save(seller=self.request.user, brand=brand, category=category)


class UpdateItem(
    viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
):
    """View for updating item information."""

    serializer_class = AddItemSerializer
    queryset = Item.objects.all()
    permission_classes = [AllowAny]
    # authentication_classes = [JWTAuthentication]
    lookup_field = "slug"

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            if request.data["brand"]:
                try:
                    brand = Brand.objects.get(id=request.data["brand"])
                    item.brand = brand
                except Brand.DoesNotExist:
                    return Response(
                        {"detail": "brand does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except:
            brand = item.brand
        category = []
        try:
            if request.data["category"]:
                try:
                    for cat in request.data["category"]:
                        category.append(Category.objects.get(id=cat))
                        item.category.add(cat)
                except Category.DoesNotExist:
                    return Response(
                        {"detail": "at least one category does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except:
            for cat in item.category.all():
                category.append(cat)
        item.save()
        serializer = self.get_serializer(item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddMedia(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for adding media (images for items) (by users)."""

    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            item = Item.objects.get(id=request.data["item"])
        except Item.DoesNotExist:
            return Response(
                {"detail": "item does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.user == item.seller:
            self.perform_create(serializer, item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "detail": "the user that is sending the request is not the user that owns the item for which the image is to be added."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def perform_create(self, serializer, item):
        serializer.save(item=item)


class AddItemSpecification(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ItemSpecificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class RemoveItemSpecification(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    queryset = ItemSpecification.objects.all()
    serializer_class = ItemSpecificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


# class UpdateMedia(viewsets.GenericViewSet, mixins.UpdateModelMixin):
#     """View for updating media (images for items) (by users)."""

#     serializer_class = MediaSerializer


class UserRegister(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for registering/creating new users."""

    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class UserList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing and retrieving all users."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_action_classes = {
        "retrieve": UserDetailSerializer,
    }
    lookup_field = "id"
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "address", "email"]

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).exclude(is_staff=True)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except:
            return self.serializer_class

    def retrieve(self, request, id=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserUpdate(
    viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
):
    """View for updating user information."""

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [
        CustomProfileUpdatePermission,
    ]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "id"


class UserPasswordUpdate(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """View for updating user password."""

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [CustomProfileUpdatePermission]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"


# class CommentDetail(viewsets.GenericViewSet, mixins.ListModelMixin):
#     """View for getting the comments for an item."""

#     # queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]
#     lookup_field = "id"

#     def get_queryset(self):
#         item_slug = self.kwargs['slug']
#         print("slug = "+item_slug)
#         return Item.objects.get(slug=item_slug).comments.all()
#         # comments = Comment.objects.get(item=item_slug)


class AddComment(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user
        self.perform_create(serializer, author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, author):
        serializer.save(author=author)


class UpdateComment(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Comment.objects.all()

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class BlackListToken(viewsets.GenericViewSet):
#     """View for blacklisting unnecessary tokens."""

#     permission_classes = [AllowAny]

#     def create(self, request):
#         try:
#             refresh_token = request.data("refresh_token")
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

# class BlackListToken(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             refresh_token = request.data['refresh_token']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

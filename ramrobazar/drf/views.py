from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ramrobazar.account.models import User
from ramrobazar.inventory.models import Brand, Category, Item
from ramrobazar.drf.serializers import MediaSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer, ItemSerializer, ItemDetailSerializer, AddItemSerializer, CategorySerializer, UserSerializer, UserDetailSerializer, UserUpdateSerializer, ChangePasswordSerializer
from ramrobazar.drf.permissions import CustomProfileUpdatePermission


"""..........................Customizing Token Claims..................................................................."""


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""..........................Customizing Token Claims End..................................................................."""


class MainView(View):
    """View for listing the endpoints."""

    def get(self, request, *args, **kwargs):
        return render(request, 'drf/main.django-html')


class CategoryList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing all categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ItemList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """View for listing and retrieving all items."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    serializer_action_classes = {'retrieve': ItemDetailSerializer, }
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__slug', 'brand__name', ]
    search_fields = ['name', 'description',
                     'category__name', 'brand__name', 'location']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except:
            return self.serializer_class

    def retrieve(self, request, slug=None):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


class AddItem(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for adding products by users."""

    serializer_class = AddItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """Try to get the brand with the id that was sent if it exists. Otherwise send an error response."""
        try:
            brand = Brand.objects.get(id=request.data['brand'])
        except Brand.DoesNotExist:
            return Response({'detail': 'brand does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        """Try to get the category with the ids that was sent if they exist. Send an error response if at least one doesn't exist."""
        category = []
        try:
            for cat in request.data['category']:
                category.append(Category.objects.get(id=cat))
        except Category.DoesNotExist:
            return Response({'detail': 'at leat one category does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer, brand, category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, brand, category):
        serializer.save(seller=self.request.user,
                        brand=brand, category=category)


class AddMedia(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for adding media (images for items) (by users)."""

    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            item = Item.objects.get(id = request.data['item'])
        except Item.DoesNotExist:
            return Response({'detail': 'item does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer, item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, item):
        serializer.save(item=item)


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
    serializer_action_classes = {'retrieve': UserDetailSerializer, }
    lookup_field = 'id'
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'address', 'email']

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


class UserUpdate(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """View for updating user information."""

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [CustomProfileUpdatePermission, ]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'


class UserPasswordUpdate(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """View for updating user password."""

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [CustomProfileUpdatePermission]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'


class BlackListToken(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """View for blacklisting unnecessary tokens."""

    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refresh_token = request.data("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

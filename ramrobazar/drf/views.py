from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ramrobazar.inventory.models import Category, Item
from ramrobazar.drf.serializers import RegisterUserSerializer, MyTokenObtainPairSerializer, ItemSerializer, ItemDetailSerializer, CategorySerializer


# ..........................Customizing Token Claims...................................................................
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
# ..........................Customizing Token Claims End...................................................................


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'drf/main.django-html')


class CategoryList(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ItemList(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    serializer_action_classes = {'retrieve': ItemDetailSerializer, }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__slug', 'brand__name',]
    search_fields = ['name', 'description', 'category__name', 'brand__name', 'location']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except:
            return self.serializer_class

    # def get_serializer(self, *args, **kwargs):
    #     # return super().get_serializer(*args, **kwargs)
    #     try:
    #         serializer_class = self.serializer_action_classes[self.action]
    #         kwargs['context'] = self.get_serializer_context()
    #         return serializer_class(*args, **kwargs)
    #     except:
    #         return super().get_serializer(*args, **kwargs)

    def retrieve(self, request, slug=None):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


# class UserRegister(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             newuser = serializer.save()
#             if newuser:
#                 return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class BlackListToken(viewsets.GenericViewSet, mixins.CreateModelMixin):
    # serializer_class =
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refresh_token = request.data("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class ProductList(viewsets.GenericViewSet, mixins.ListModelMixin):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny]
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, mixins, status
# from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ramrobazar.inventory.models import Category, ProductOrService
from ramrobazar.drf.serializers import RegisterUserSerializer, MyTokenObtainPairSerializer, ProductOrServiceSerializer, ProductOrServiceDetailSerializer, CategorySerializer


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


class ProductsOrServicesList(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ProductOrService.objects.all()
    serializer_class = ProductOrServiceSerializer
    serializer_action_classes = {'retrieve': ProductOrServiceDetailSerializer, }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except:
            return self.serializer_class

    def retrieve(self, request, slug=None):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


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
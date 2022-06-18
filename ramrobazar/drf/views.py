from rest_framework import viewsets, permissions, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ramrobazar.inventory.models import ProductOrService
from ramrobazar.drf.serializers import ProductOrServiceSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer



#..........................Customizing Token Claims...................................................................
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
#..........................Customizing Token Claims End...................................................................


class ProductsOrServicesList(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = ProductOrService.objects.all()
    serializer_class = ProductOrServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = ProductOrService.objects.filter(category__slug=slug)
        serializer = ProductOrServiceSerializer(queryset, many=True)
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
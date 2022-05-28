from unicodedata import category
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from ramrobazar.inventory.models import Product
from ramrobazar.drf.serializers import AllProductsSerializer


class AllProductsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(category__slug=slug)
        serializer = AllProductsSerializer(queryset, many=True)
        return Response(serializer.data)
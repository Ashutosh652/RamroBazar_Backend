# from pyexpat import model
from rest_framework import serializers
from ramrobazar.inventory.models import Product, Brand

# class ProductAttributeValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttributeValue
#         exclude = ['id']
#         depth = 2

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name',]


class AllProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['name',]
        read_only = True
        editable = False


# class ProductInventorySerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(many=False, read_only=True)
#     attribute_value = ProductAttributeValueSerializer(many=True)

#     class Meta:
#         model = ProductInventory
#         fields = ['product_type', 'product', 'brand', 'attribute_value', 'sold', 'is_visible', 'price', 'weight']
#         read_only = True
#         # depth = 2
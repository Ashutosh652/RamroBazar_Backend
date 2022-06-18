# from pyexpat import model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ramrobazar.inventory.models import Product, Brand, ProductOrService
from ramrobazar.account.models import User



#..........................Customizing Token Claims...................................................................
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['contact_number'] = str(user.contact_number)
        return token
#..........................Customizing Token Claims End...................................................................

# class ProductAttributeValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttributeValue
#         exclude = ['id']
#         depth = 2

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name',]


class ProductOrServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductOrService
        # fields = '__all__'
        exclude = ['id',]
        read_only = True
        editable = False
        depth = 0


# class ProductInventorySerializer(serializers.ModelSerializer):
#     brand = BrandSerializer(many=False, read_only=True)
#     attribute_value = ProductAttributeValueSerializer(many=True)

#     class Meta:
#         model = ProductInventory
#         fields = ['product_type', 'product', 'brand', 'attribute_value', 'sold', 'is_visible', 'price', 'weight']
#         read_only = True
#         # depth = 2


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['contact_number', 'first_name', 'last_name', 'password']
        extra_kwargs = { 'password' : { 'write_only' : True } }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
# from pyexpat import model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ramrobazar.inventory.models import Category, Product, Brand, ProductOrService, Service
from ramrobazar.account.models import User
from ramrobazar.settings import BASE_URL


# ..........................Customizing Token Claims...................................................................
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['contact_number'] = str(user.contact_number)
        return token
# ..........................Customizing Token Claims End...................................................................

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField(source='get_parent')

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent',]
    
    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['name',]


class ProductOrServiceSerializer(serializers.HyperlinkedModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name='drf:productsandservices-detail', lookup_field='slug')

    class Meta:
        model = ProductOrService
        fields = ['name', 'detail', 'web_id', 'slug',
                  'is_visible', 'is_blocked', 'is_product', ]
        # exclude = ['id',]
        read_only = True
        editable = False
        depth = 0


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['brand', 'show_price', 'available_units', 'sold_units',]
        read_only = True
        # lookup_field = 'slug'
        # depth = 2


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
        # lookup_field = 'slug'


class ProductOrServiceDetailSerializer(serializers.ModelSerializer):
    
    # if ProductOrService.is_product:
    #     product = ProductSerializer(many=False, read_only=True)
    # elif not ProductOrService.is_product:
    #     service = ServiceSerializer(many=False, read_only=True)
    product = ProductSerializer(many=False, read_only=True)
    service = ServiceSerializer(many=False, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ProductOrService
        # exclude = ['id',]
        fields = ['product', 'service', 'web_id', 'slug', 'name', 'description', 'is_visible', 'is_blocked', 'created_at', 'updated_at', 'is_product', 'seller', 'category', 'users_wishlist', 'reported_by',]
        # if ProductOrService.is_product:
        #     fields = ['product', 'web_id', 'slug', 'name', 'description', 'is_visible', 'is_blocked', 'created_at', 'updated_at', 'is_product', 'seller', 'category', 'users_wishlist', 'reported_by',]
        # elif not ProductOrService.is_product:
        #     fields = ['service', 'web_id', 'slug', 'name', 'description', 'is_visible', 'is_blocked', 'created_at', 'updated_at', 'is_product', 'seller', 'category', 'users_wishlist', 'reported_by',]
        read_only = True
        editable = False
        lookup_field = 'slug'


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['contact_number', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

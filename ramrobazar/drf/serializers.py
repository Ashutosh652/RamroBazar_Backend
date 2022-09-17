from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ramrobazar.inventory.models import Category, Brand, Item, Media
from ramrobazar.account.models import User


"""..........................Customizing Token Claims..................................................................."""


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Overriding the default token serializer class so that the token contains additional information."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['contact_number'] = str(user.contact_number)
        token['first_name'] = str(user.first_name)
        token['last_name'] = str(user.last_name)
        return token


"""..........................Customizing Token Claims End..................................................................."""


class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for lowest level category that has no children."""

    parent = serializers.SerializerMethodField(source='get_parent')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', ]

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    parent = serializers.SerializerMethodField(source='get_parent')
    children = serializers.SerializerMethodField(source='get_children')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children', ]

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
    
    def get_children(self, obj):
        if obj.children.exists():
            children = [child for child in obj.children.all()]
            children_with_children = [child for child in children if child.children.exists()]
            children_without_children = [child for child in children if not child.children.exists()]
            if children_with_children:
                return CategorySerializer(children_with_children, many=True).data
            if children_without_children:
                return SubCategorySerializer(children_without_children, many=True).data

class BrandSerializer(serializers.ModelSerializer):
    """Serializer for brand."""

    class Meta:
        model = Brand
        fields = ['id', 'name', ]


class MediaSerializer(serializers.ModelSerializer):
    """Serializer for media (images of items)."""

    image = serializers.ImageField(required=False)

    class Meta:
        model = Media
        fields = ['id', 'image', 'alt_text', 'is_feature', 'item', ]
        read_only = True


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for items (for listing purpose)."""

    detail = serializers.HyperlinkedIdentityField(
        view_name='drf:items-detail', lookup_field='slug')
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'detail', 'slug', 'media',
                  'is_visible', 'is_blocked', 'show_price', 'description', ]
        read_only = True
        editable = False
        depth = 0


class ItemDetailSerializer(serializers.ModelSerializer):
    """Serializer for items (for retrieving/detail purpose)."""

    category = CategorySerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'slug', 'name', 'description', 'brand', 'show_price', 'sold_times', 'location', 'is_visible',
                  'is_blocked', 'created_at', 'updated_at', 'seller', 'category', 'media', 'users_wishlist', 'reported_by']
        read_only = True
        editable = False
        lookup_field = 'slug'


class AddItemSerializer(serializers.ModelSerializer):
    """Serializer for adding items (by users)."""

    brand = BrandSerializer(many=False, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'brand', 'show_price',
                  'location', 'is_visible', 'category']


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for registering new user."""

    class Meta:
        model = User
        fields = ['contact_number', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for changing user's password."""

    current_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password1', 'new_password2']

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {'new_password1': 'New Password fields did not match.'})
        elif not user.check_password(attrs['current_password']):
            raise serializers.ValidationError(
                {"current_password": "Current password is not correct."})
        elif attrs['new_password1'] == attrs['new_password2']:
            return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users (for listing purpose)."""

    detail = serializers.HyperlinkedIdentityField(
        view_name='drf:users-detail', lookup_field='id')

    class Meta:
        model = User
        fields = ['id', 'detail', 'first_name', 'last_name', 'profile_pic']
        read_only = True
        editable = False


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for users (for retrieving/detail purpose)."""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'contact_number', 'date_joined', 'is_contact_number_verified', 'is_blocked',
                  'is_active', 'email', 'is_email_verified', 'address', 'profile_pic', 'date_of_birth', 'no_sold_items']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user detail/information."""

    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_pic',
                  'contact_number', 'email', 'address', 'date_of_birth']

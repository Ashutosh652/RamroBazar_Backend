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


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    parent = serializers.SerializerMethodField(source='get_parent')

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', ]

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for brand."""

    class Meta:
        model = Brand
        fields = ['name', ]


class MediaSerializer(serializers.ModelSerializer):
    """Serializer for media (images of items)."""

    class Meta:
        model = Media
        fields = ['image', 'alt_text', 'is_feature', ]
        read_only = True


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for items (for listing purpose)."""

    detail = serializers.HyperlinkedIdentityField(
        view_name='drf:items-detail', lookup_field='slug')
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['name', 'detail', 'web_id', 'slug', 'media',
                  'is_visible', 'is_blocked', 'show_price', ]
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
        fields = ['web_id', 'slug', 'name', 'description', 'brand', 'show_price', 'sold_times', 'location', 'is_visible',
                  'is_blocked', 'created_at', 'updated_at', 'seller', 'category', 'media', 'users_wishlist', 'reported_by', ]
        read_only = True
        editable = False
        lookup_field = 'slug'


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

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'contact_number', 'email', 'address', 'date_of_birth']

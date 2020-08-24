from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Product


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'width', 'depth', 'height', 'weight', 'price')

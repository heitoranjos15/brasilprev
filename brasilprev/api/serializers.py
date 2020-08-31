from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'width', 'depth', 'height', 'weight', 'price')


class OrderSerializer(serializers.Serializer):
    products = serializers.ListField(child=serializers.DictField())

    def create(self, validated_data):
        order = Order.objects.create(client_id=self.context['request'].user)
        for item in validated_data['products']:
            orderItem = OrderItem()
            orderItem.order = order
            orderItem.product = Product.objects.get(pk=item['product_id'])
            orderItem.quantity = item['product_quantity']
            orderItem.save()
        return order

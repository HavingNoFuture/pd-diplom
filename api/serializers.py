from rest_framework import serializers

from app.models import Order, Cart, CartItem, ProductInfo, Product, Shop


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("name", "state")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name",)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductInfo
        fields = ("product", "price")


class CartItemSerializer(serializers.ModelSerializer):
    productinfo = ProductInfoSerializer()
    class Meta:
        model = CartItem
        fields = ("productinfo", "quantity", "item_total")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ("items", "cart_total")


class OrderFullSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = ("id", "create_date", "comment", "status", "cart", "address")


class OrderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "create_date")
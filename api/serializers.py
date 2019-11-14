from rest_framework import serializers

from app.models import Order, Cart, CartItem, ProductInfo, Product, Shop


SHOP_STATE_CHOICES = (
    ('on', 'on'),
    ('off', 'off')
)


class ShopSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=SHOP_STATE_CHOICES)

    class Meta:
        model = Shop
        fields = ("id", "name", "state")
        read_only_fields = ('id', 'url', "name")


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


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = ("id", "create_date", "comment", "status", "cart", "address")

from rest_framework import serializers

from app.models import Order, Cart, CartItem, ProductInfo, Product, Shop


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Использую, чтобы доставать определенные поля из ModelSerializer
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ShopListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # validated_data = [{'id': 7, 'state': 'on'}]  # такой должна стать
        print('validation_data: ', validated_data)

        # Maps for id->instance and id->data item.
        shop_mapping = {shop.id: shop for shop in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for shop_id, data in data_mapping.items():
            shop = shop_mapping.get(shop_id, None)
            if shop is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(shop, data))

        return ret


class ShopSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Shop
        fields = ("id", "url", "state")
        list_serializer_class = ShopListSerializer


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


class OrderSerializer(DynamicFieldsModelSerializer):
    cart = CartSerializer()
    class Meta:
        model = Order
        fields = ("id", "create_date", "comment", "status", "cart", "address")

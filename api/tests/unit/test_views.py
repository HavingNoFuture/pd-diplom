from django.test import TestCase, Client

from app.models import Order, Cart, User, CartItem, ProductInfo, Product, Shop, Category

# # Create your tests here.
# class GetOrderListViewTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         pass
#
#     def setUp(self):
#         user = User.objects.get(pk=1)
#         shop = Shop.objects.create(name="Test_shop", url="url.com")
#         category = Category.objects.create(name="Test_category", shops=[shop])
#         product1 = Product.objects.create(name="Test_product1", category=category, model="Test_model1", description="Test_comment1")
#         product2 = Product.objects.create(name="Test_product2", category=category, model="Test_model2", description="Test_comment2")
#         product_info1 = ProductInfo.objects.create(product=product1, shop=shop, quantity=6, price=34.00)
#         product_info2 = ProductInfo.objects.create(product=product2, shop=shop, quantity=4, price=65.00)
#         items = []
#         items.append(CartItem.objects.create(productinfo=product_info1, quantity=2))
#         items.append(CartItem.objects.create(productinfo=product_info2, quantity=1))
#         cart = Cart.objects.create(items=items)
#         Order.objects.create(user=user, first_name="Alex", last_name="Erm", second_name="Nik",
#                              phone=423424, cart=cart, comment="Comment")
#
#     def
from django.test import TestCase

from app.models import Category, Product, Shop, ProductInfo, Cart, CartItem, Order


class ShopModelTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="Test_shop_name")

    def testStr(self):
        self.assertEqual(self.shop.__str__(), "Test_shop_name")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test_category_name")

    def testStr(self):
        self.assertEqual(self.category.__str__(), "Test_category_name")
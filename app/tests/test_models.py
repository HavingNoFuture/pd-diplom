from django.test import TestCase
from django.urls import reverse

from app.models import Category, Product, Shop, ProductInfo, Cart, CartItem, Order, User, Parameter, ProductParameter, Contact


def create_order(self):
    self.user = User.objects.create(email="test_email.com", first_name="Alex", last_name="Erm", second_name="Nik")
    self.shop = Shop.objects.create(name="Test_shop", url="url.com")
    self.category = Category.objects.create(name="Test_category")
    self.category.save()
    self.category.shops.add(self.shop)
    self.category.save()
    self.product1 = Product.objects.create(name="Test_product1", category=self.category, model="Test_model1", description="Test_comment1")
    self.product2 = Product.objects.create(name="Test_product2", category=self.category, model="Test_model2", description="Test_comment2")
    self.product_info1 = ProductInfo.objects.create(product=self.product1, shop=self.shop, quantity=6, price=34.00)
    self.product_info2 = ProductInfo.objects.create(product=self.product2, shop=self.shop, quantity=4, price=65.00)
    self.cart_item1 = CartItem.objects.create(productinfo=self.product_info1, quantity=2)
    self.cart_item2 = CartItem.objects.create(productinfo=self.product_info2, quantity=1)
    self.cart = Cart(id=1)
    self.cart.save()
    self.cart.items.add(self.cart_item1, self.cart_item2)
    self.cart.save()
    self.order = Order.objects.create(user=self.user, first_name="Alex", last_name="Erm", second_name="Nik",
                             phone=423424, cart=self.cart, comment="Comment")
    self.parameter = Parameter.objects.create(name="Test_parameter")
    self.product_parameter = ProductParameter.objects.create(product_info=self.product_info1, parameter=self.parameter, value="10")


class ShopModelTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="Test_shop_name")

    def test_str_method(self):
        self.assertEqual(self.shop.__str__(), "Test_shop_name")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test_category_name")

    def test_str_method(self):
        self.assertEqual(self.category.__str__(), "Test_category_name")

    def test_abs_url(self):
        url = reverse('category', kwargs={'slug': self.category.slug})
        self.assertEqual(self.category.get_absolute_url(), url)


class ProductModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.product1.__str__(), "Test_product1")

    def test_abs_url(self):
        url = reverse('product', kwargs={'slug': self.product1.slug})
        self.assertEqual(self.product1.get_absolute_url(), url)


class ProductInfoModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.product_info1.__str__(), "Test_product1 - Product Info")


class ParameterModelTest(TestCase):
    def setUp(self):
        self.parameter = Parameter.objects.create(name="Test_parameter")

    def test_str_method(self):
        self.assertEqual(self.parameter.__str__(), "Test_parameter")


class ProductParameterModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.product_parameter.__str__(), "Test_product1 - Test_parameter")


class CartItemModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.cart_item1.__str__(), "Cart item №1")


class CartModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.cart.__str__(), "Cart №1")

    def test_add_to_cart(self):
        self.cart.add_to_cart(self.product_info2)
        # Проверяю, что product_info после добавления одинаковые
        exp_product_info = self.cart.items.all()[1].productinfo
        self.assertEqual(exp_product_info, self.product_info2)

        # Проверяю, что после добавления quantity == 1
        exp_quantity = self.cart.items.all()[1].quantity
        self.assertEqual(exp_quantity, 1)

    def test_remove_from_cart(self):
        self.cart.remove_from_cart(self.cart_item2)
        self.assertNotIn(self.cart_item2, self.cart.items.all())


class OrderModelTest(TestCase):
    def setUp(self):
        create_order(self)

    def test_str_method(self):
        self.assertEqual(self.order.__str__(), "Заказ №1")

class ContactModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(email="test_email.com", first_name="Alex", last_name="Erm", second_name="Nik")
        self.contact = Contact.objects.create(user=user, value='88005553535')

    def test_str_method(self):
        self.assertEqual(self.contact.__str__(), "1")

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test_email.com", first_name="Alex", last_name="Erm",
                                   second_name="Nik")

    def test_str_method(self):
        self.assertEqual(self.user.__str__(), "test_email.com - Alex Erm")

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Alex Nik Erm")

    def test_get_name(self):
        self.assertEqual(self.user.get_name(), "Alex Erm")

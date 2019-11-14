from django.test import TestCase
from django.urls import reverse

from app.models import Category, Product, Shop, ProductInfo, Cart, CartItem, Order, User, Parameter, ProductParameter, Contact

class CatalogViewTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="Test_shop_name")

    def test_str_method(self):
        self.assertEqual(self.shop.__str__(), "Test_shop_name")


    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/shop/catalog/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('catalog'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('catalog'))
        self.assertTemplateUsed(resp, 'app/catalog.html')

    #
    # category = request.GET.get('category')
    # shop = request.GET.get('shop')
    #
    # context = {}
    # products = Product.objects.all()
    #
    # if category:
    #     products = Product.objects.filter(category__name__iexact=category)
    #
    # if shop:
    #     productinfos = ProductInfo.objects.filter(shop__name__iexact=shop)
    #     products = []
    #     for productinfo in productinfos:
    #         products.append(productinfo.product)
    #
    # context["products"] = products
    # context['shops'] = Shop.objects.all()
    # context['categories'] = Category.objects.all()
    #
    # return render(request, 'app/catalog.html', context)
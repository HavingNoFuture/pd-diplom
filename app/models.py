from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings

from django.utils.text import slugify
from django.db.models.signals import pre_save

from transliterate import translit


from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

from decimal import Decimal


USER_TYPE_CHOICES = (
    ('Покупатель', 'Покупатель'),
    ('Продавец', 'Продавец')
)

USER_STATE_CHOICES = (
    ('on', 'on'),
    ('off', 'off')
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    second_name = models.CharField(_('second_name'), max_length=30, blank=True)
    company = models.CharField(_('company'), max_length=100, blank=True)
    position = models.CharField(_('position'), max_length=100, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES, default='Покупатель')
    state = models.CharField(max_length=3, choices=USER_STATE_CHOICES, default='off')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.email} - {self.get_name()}'

    def get_full_name(self):
        return f'{self.first_name} {self.second_name} {self.last_name}'

    def get_name(self):
        return f'{self.first_name} - {self.last_name}'

    def is_staff(self): # ?
        return True



CONTACT_TYPE_CHOICES = (
    ('Телефон', 'Телефон'),
    ('Адрес', 'Адрес'),
)

class Contact(models.Model):
    type = models.CharField(max_length=100, choices=CONTACT_TYPE_CHOICES, default='Телефон')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.pk}'


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            instance.slug = slugify(translit(instance.name, reversed=True))
        except:
            instance.slug = slugify(instance.name)


class Shop(models.Model):
    name = models.CharField(max_length=90)
    url = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    logo = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('shop', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Shop)


class Category(models.Model):
    name = models.CharField(max_length=30)
    shops = models.ManyToManyField('Shop', related_name='categories')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('category', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Category)


class Manufacturer(models.Model):
	name = models.CharField(max_length=120)
	logo = models.ImageField()


class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length = 120)
    slug = models.SlugField(blank=True)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_info(self): # ?
        return f'{self.name} {self.category}'

    def get_absolute_url(self):
      return reverse('product', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Product)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} - Product Info'


class Parameter(models.Model):
    name = models.CharField(max_length = 120)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=90)

    def __str__(self):
        return f'{self.product.name} - {self.parameter}'


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class CartItem(models.Model):
    productinfo = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, blank=True)

    def __str__(self):
        return f'Cart item for product {self.productinfo.product.name}'


    def count_item_total(self):
        self.item_total = Decimal(self.productinfo.price) * Decimal(self.quantity)
        self.save()


    def change_quantity(self, quantity):
        self.quantity = quantity
        self.save()
        self.count_item_total()


    def change_productinfo(self, productinfo):
        self.productinfo = productinfo
        self.save()



class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.pk}'

    def add_to_cart(self, productinfo):
        cart = self
        print(productinfo)
        new_item, _ = CartItem.objects.get_or_create(productinfo=productinfo)
        print(new_item.productinfo.pk)

        if new_item not in cart.items.all():
            new_item.quantity = 1
            new_item.save()
            new_item.count_item_total()
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, cartitem):
        cart = self
        for cart_item in cart.items.all():
            if cart_item == cartitem:
                cart.items.remove(cart_item)
                cart.save()

    def count_cart_total(self):
        cart = self
        new_cart_total = Decimal(0.00)
        for item in cart.items.all():
            new_cart_total += Decimal(item.item_total)

        cart.cart_total = new_cart_total
        cart.save()
        return cart.cart_total


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True)
    phone = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')), default='Самовывоз')
    address = models.CharField(max_length=500, default='Самовывоз', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Принят в обработку')

    def __str__(self):
        return f'Заказ №{self.pk}'

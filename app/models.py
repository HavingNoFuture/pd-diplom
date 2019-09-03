from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings

from django.utils.text import slugify
from django.db.models.signals import pre_save

from transliterate import translit


from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    second_name = models.CharField(_('second_name'), max_length=30)
    company = models.CharField(_('company'), max_length=100)
    position = models.CharField(_('position'), max_length=100)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

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

    def is_staff(self):
        return True


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            instance.slug = slugify(translit(instance.name, reversed=True))
        except:
            instance.slug = slugify(instance.name)



class Shop(models.Model):
    name = models.CharField(max_length=90)
    url = models.CharField(max_length=120)
    filename = models.CharField(max_length=90)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Shop)


class Category(models.Model):
    ida = models.PositiveIntegerField() 
    name = models.CharField(max_length=30)
    shops = models.ManyToManyField('Shop', related_name='categories')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Category)


class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_info(self): # ?
        return f'{self.name} {self.category}'

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})

pre_save.connect(pre_save_slug, sender=Product)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    model = models.CharField(max_length = 120) # ?
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField() # ?

    def __str__(self):
        return f'{self.product.name} - Product Info'

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


class Parameter(models.Model):
    name = models.CharField(max_length = 120)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=90) # ?

    def __str__(self):
        return f'{self.product_info.product.name} - {self.parameter}'

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dt = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Принят в обработку')

    def __str__(self):
        return self.pk

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.pk

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


CONTACT_TYPE_CHOICES = (
    ('Телефон', 'Телефон'),
    ('Адрес', 'Адрес'),
)


class Contact(models.Model):
    type = models.CharField(max_length=100, choices=CONTACT_TYPE_CHOICES, default='Телефон')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.pk

    # def get_absolute_url(self):
    #   return reverse('category', kwargs={'slug': self.slug})


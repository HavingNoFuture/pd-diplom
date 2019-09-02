from django.db import models
from django.urls import reverse
from django.conf import settings

from django.utils.text import slugify
from django.db.models.signals import pre_save

from transliterate import translit


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
        return f'{name} {category}'

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


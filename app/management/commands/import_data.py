# -*- coding: utf-8 -*-
import yaml

from django.conf  import settings
import os

from django.core.management.base import BaseCommand
from app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter

BASE_DIR = r'D:\python_projects\django_projects\pd-diplom'
# print(settings.BASE_DIR)
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # with open(f'{settings.BASE_DIR}{os.sep}data{os.sep}shop1.yaml', 'r') as stream:
        with open(f'{BASE_DIR}{os.sep}data{os.sep}shop1.yaml', 'r', encoding='utf8') as stream:
            try:
                data = yaml.safe_load(stream)
                
                shop = Shop.objects.create(
                    name = data['shop'],
                )


                categories = []
                for ctgry in data['categories']:
                    category = Category.objects.create(
                        ida = ctgry['id'],
                        name = ctgry['name']
                    )
                    shop.categories.add(category)
                    shop.save()


                for prdct in data['goods']:
                    product = Product.objects.create(
                        pk = prdct['id'],
                        category = Category.objects.get(ida=int(prdct['category'])), # ?
                        name = prdct['name']
                    )

                    product_info = ProductInfo.objects.create(
                        product = product,
                        shop = shop,
                        model = prdct['model'], # ?
                        price = prdct['price'],
                        price_rrc = prdct['price_rrc'],
                        quantity = prdct['quantity'],
                    )

                    for parameter_name, parameter_value in prdct['parameters'].items():
                        try:
                            parameter = Parameter.objects.get(name=parameter_name)
                        except Parameter.DoesNotExist:
                            parameter = Parameter.objects.create(
                                name = parameter_name
                            )

                        ProductParameter.objects.create(
                            product_info = product_info,
                            parameter = parameter,
                            value = parameter_value
                        )

            except yaml.YAMLError as exc:
                print(exc)

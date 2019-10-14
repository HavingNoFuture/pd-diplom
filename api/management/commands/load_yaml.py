import yaml

from django.core.management.base import BaseCommand
from app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, stream, *args, **options):

        try:
            data = yaml.safe_load(stream)

            # Этот код использую, чтобы предотвратить создание магазина от левых челов
            # try:
            #     shop = Shop.objects.get_or_create(name=data['shop'])
            # except Shop.DoesNotExist as e:
            #     return {'Status': 'Error', "Error": "Магазина не существует. Обратитесь к администратору сайта"}

            shop = Shop.objects.get_or_create(name=data['shop'])[0]

            for ctgry in data['categories']:
                category = Category.objects.get_or_create(
                    id=ctgry['id'],
                    name=ctgry['name']
                )[0]
                shop.categories.add(category)
                shop.save()

            for prdct in data['goods']:
                product = Product.objects.get_or_create(
                    pk=prdct['id'],
                    category=Category.objects.get(id=int(prdct['category'])),
                    name=prdct['name'],
                    model=prdct['model']
                )[0]

            product_info = ProductInfo.objects.create(
                product=product,
                shop=shop,
                price=prdct['price'],
                quantity=prdct['quantity']
            )

            for parameter_name, parameter_value in prdct['parameters'].items():
                parameter = Parameter.objects.get_or_create(name=parameter_name)[0]

                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=parameter_value
                )

            return {'Status': 'Success'}

        except yaml.YAMLError as exc:
            print(exc)

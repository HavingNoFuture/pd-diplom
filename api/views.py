# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app.models import Order, Shop

from api.serializers import OrderSerializer, ShopSerializer
from api.permissions import IsShopAdmin
from api.management.commands.load_yaml import Command


# API's views

class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Получить список заказов.
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True, fields=('id', 'create_date'))
        return Response({"orders": serializer.data})

    def retrieve(self, request, pk=None):
        # Получить детали заказа по id.
        queryset = self.queryset.filter(user=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(order)
        return Response({"order": serializer.data})


class StateViewSet(viewsets.ViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsShopAdmin, IsAdminUser]

    def list(self, request):
        """Получить текущий статус всех контролируемых магазинов."""
        queryset = self.queryset.filter(user_admins=request.user)
        serializer = self.serializer_class(queryset, many=True, fields=('name', 'state'))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Получить текущий статус контролируемого магазина по id."""
        queryset = self.queryset.filter(user_admins=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(order, fields=('name', 'state'))
        return Response({"order": serializer.data})

    def partial_update(self, request, pk=None):
        state = request.data.get('state')
        queryset = self.queryset.filter(user_admins=request.user)

        shop = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(shop, data=request.data, fields=('state'))
        if serializer.is_valid() and state in ('on', 'off'):
            serializer.save(state=state)
        return Response({
            'shop_id': pk,
            'state': shop.state
        })

    def create(self, request):
        # Изменить статус всех магазинов, контролируемых пользователем.
        state = request.data.get('state')
        queryset = self.queryset.filter(user_admins=request.user)

        shop_id_list = [shop['id'] for shop in queryset.values()]  # shop_id_list == [7]
        data = [{'id': id, 'state': state} for id in shop_id_list]  # data == [{'id': 7, 'state': 'on'}]

        serializer = self.serializer_class(queryset, data=data, fields=('pk', 'state'), many=True)
        if serializer.is_valid() and state in ('on', 'off'):
            serializer.save()

        return Response(serializer.data)

# TODO: удалить перед релизом
from django.conf import settings

class PriceUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsShopAdmin, IsAdminUser]

    def list(self, request):
        # TODO: удалить перед релизом
        # Тест. Работает с локалки
        filename = fr'{settings.BASE_DIR}\data\shop1.yaml'
        print(filename)
        with open(filename, 'r', encoding='utf-8') as stream:
            load_yaml = Command()
            e = load_yaml.handle(stream)
            return Response({str(e)})


    def create(self, request, *args, **kwargs):
        """Обновление ассортимента магазина с yaml url."""
        url = request.data.get('url')

        load_yaml = Command()
        output = load_yaml.handle(url)
        return Response({str(output)})

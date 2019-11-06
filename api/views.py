# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from app.models import Order, Shop

from api.serializers import OrderSerializer, ShopSerializer
from api.permissions import IsShopAdmin
from api.management.commands.load_yaml import Command


# API's views

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='', url_name='get-order-list')
    def get_order_list(self, request):
        # Получить список заказов.
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"orders": serializer.data})

    @action(methods=['get'], detail=True, url_path='', url_name='get-order-detail')
    def get_order_detail(self, request, pk=None):
        # Получить детали заказа по id.
        queryset = self.queryset.filter(user=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(order)
        return Response({"order": serializer.data})


class StateViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsShopAdmin, IsAdminUser]

    @action(methods=['get'], detail=False, url_path='', url_name='get-state-list')
    def get_state_list(self, request):
        """Получить текущий статус всех контролируемых магазинов."""

        queryset = self.queryset.filter(user_admins=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='', url_name='get-state-detail')
    def get_state_detail(self, request, pk=None):
        """Получить текущий статус магазина по id."""

        queryset = self.queryset.filter(user_admins=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(order)
        return Response({"shop_info": serializer.data})

    @action(methods=['post'], detail=True, url_path='', url_name='update-state-detail')
    def update_state_detail(self, request, pk=None):
        """Изменить текущий статус магазина по id."""

        queryset = self.queryset.filter(user_admins=request.user)
        shop = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(shop, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    @action(methods=['post'], detail=False, url_path='', url_name='update-state-list')
    def update_state_list(self, request):
        """Изменить статус всех магазинов, контролируемых пользователем."""

        state = request.data.get('state')
        queryset = self.queryset.filter(user_admins=request.user)

        shop_list, errors_list = [], []
        for shop in queryset:
            serializer = self.serializer_class(shop, data=request.data)
            if serializer.is_valid():
                shop.state = state
                shop_list.append(shop)
            else:
                errors_list.append(serializer.errors)

        Shop.objects.bulk_update(shop_list, fields=('state',))

        if errors_list:
            return Response({'Status': False, 'Errors': errors_list})

        return Response({'Status': True})


# TODO: удалить перед релизом
from django.conf import settings

class PriceUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsShopAdmin, IsAdminUser]

    @action(methods=['get'], detail=False, url_path='', url_name='update-price-local')
    def update_price_local(self, request):
        # TODO: удалить перед релизом
        # Тест. Работает с локалки

        filename = fr'{settings.BASE_DIR}\data\shop1.yaml'
        print(filename)
        with open(filename, 'r', encoding='utf-8') as stream:
            load_yaml = Command()
            e = load_yaml.handle(stream)
            return Response({str(e)})

    @action(methods=['post'], detail=False, url_path='', url_name='update-price')
    def update_price(self, request, *args, **kwargs):
        """Обновление ассортимента магазина с yaml url."""

        url = request.data.get('url')
        load_yaml = Command()
        output = load_yaml.handle(url)
        return Response({str(output)})

# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from django.core.exceptions import PermissionDenied

from app.models import Order, Shop

from api.serializers import OrderSerializer, ShopSerializer
from api.permissions import IsShopAdmin
from api.management.commands.load_yaml import Command
from api.tasks import do_import


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'orders'

    def get_queryset(self, *args, **kwargs): 
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get_object(self, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs['pk']
        try:
            order = self.queryset.get(pk=pk, user=user)
        except Order.DoesNotExist:
            raise PermissionDenied()
        return order


class StateViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsShopAdmin, IsAdminUser]
    throttle_scope = 'states'

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user_admins=self.request.user)
        return queryset

    def get_object(self, *args, **kwargs):

        pk = self.kwargs['pk']
        try:
            shop_info = self.get_queryset().get(pk=pk)
        except Shop.DoesNotExist:
            raise PermissionDenied()
        return shop_info

    @action(methods=['post'], detail=True, url_path='', url_name='update-state-detail')
    def update_state_detail(self, request, pk=None):
        """Изменить текущий статус магазина по id."""

        try:
            shop = self.get_queryset().get(pk=pk)
        except Shop.DoesNotExist:
            raise PermissionDenied()

        serializer = self.serializer_class(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    @action(methods=['post'], detail=False, url_path='', url_name='update-state-list')
    def update_state_list(self, request):
        """Изменить статус всех магазинов, контролируемых пользователем."""

        state = request.data.get('state')
        queryset = self.get_queryset()

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


class PriceUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsShopAdmin, IsAdminUser]
    throttle_scope = 'uploads'


    def update_price(self, request, *args, **kwargs):
        """Обновление ассортимента магазина с yaml url."""

        url = request.data.get('url')
        output = do_import(url)
        return Response({str(output)})

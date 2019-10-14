# -*- coding: utf-8 -*-
from requests import get

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from api.management.commands.load_yaml import Command

from app.models import Order, Shop
from api.serializers import OrderShortSerializer, StateSerializer, OrderFullSerializer


# API's views

class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        try:
            # Получить детали заказа по id.
            id = int(kwargs['id'])
            order = Order.objects.get(pk=id)
            serializer = OrderFullSerializer(order)
            return Response({"order": serializer.data})
        except KeyError:
            # Получить список заказов.
            queryset = Order.objects.filter(user=request.user)
            serializer = OrderShortSerializer(queryset, many=True)
            return Response({"orders": serializer.data})


class StateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """Получить текущий статус магазина по id."""
        shop = request.user.controlled_shop.all()
        serializer = StateSerializer(shop, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Изменить статус магазина."""
        user = request.user
        state = request.data.get('state')

        try:
            id = int(kwargs['id'])
            try:
                shop = Shop.objects.get(pk=id)
            except Shop.DoesNotExist as e:
                return Response({'Status': False, 'Error': str(e)})

            if user not in shop.user_admins.all():
                return Response({'Status': False, 'Errors': 'У вас нет прав редактирования этого магазина.'})

            if state and state in ('on', 'off'):
                try:
                    shop.state=state
                    return Response({'Status': True})
                except ValueError as e:
                    return Response({'Status': False, 'Errors': str(e)})
            return Response({'Status': False, 'Errors': 'State не прошел сериализацию.'})

        except KeyError as e:
            try:
                Shop.objects.filter(user_admins=request.user.id).update(state=str(state))
                return Response({'Status': True})
            except ValueError as error:
                return Response({'Status': False, 'Errors': str(error)})


from django.conf import settings

class PriceUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        """test
        Обновление ассортимента магазина из файла yaml.
        """
        load_yaml = Command()

        with open(f'{settings.BASE_DIR}/data/shop1.yaml', 'r', encoding='utf-8') as stream:
            result = load_yaml.handle(stream)

        return Response(result)

    def post(self, request, *args, **kwargs):
        """Обновление ассортимента магазина с yaml url."""
        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return Response({'Status': False, 'Errors': str(e)})
            else:
                stream = get(url).content

                load_yaml = Command()
                load_yaml.handle(stream)
                return Response({'Status': True})

# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from app.models import Order

from api.serializers import OrderShortSerializer, StateSerializer, OrderFullSerializer
from api.management.commands.load_yaml import Command


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests import get





# API's views

class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        try:
            id = int(kwargs['id'])
            order = Order.objects.get(pk=id)
            serializer = OrderFullSerializer(order)
            return Response({"order": serializer.data})
        except KeyError:
            queryset = Order.objects.filter(user=request.user)
            serializer = OrderShortSerializer(queryset, many=True)
            return Response({"orders": serializer.data})


class StateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"state": user.state})

    def post(self, request, *args, **kwargs):
        user = request.user


        serializer = StateSerializer(data={'state': "on"})


        if serializer.is_valid():
            serializer.save(user=user)
            # print(serializer.data)
            # user.state = serializer.data
            # user.save()

        # Работающий пример
        # user.state = request.data['state']
        # user.save()
        return Response()

#
# # получить текущий статус
# def get(self, request, *args, **kwargs):
#     shop = request.user.shop
#     serializer = ShopSerializer(shop)
#     return Response(serializer.data)
#
#
# # изменить текущий статус
# def post(self, request, *args, **kwargs):
#     state = request.data.get('state')
#     if state:
#         try:
#             Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
#             return JsonResponse({'Status': True})
#         except ValueError as error:
#             return JsonResponse({'Status': False, 'Errors': str(error)})
#     return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
#
#
#






from django.conf import settings

class PriceUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        load_yaml = Command()

        with open(f'{settings.BASE_DIR}/data/shop1.yaml', 'r', encoding='utf-8') as stream:
            result = load_yaml.handle(stream)

        return Response(result)

    def post(self, request, *args, **kwargs):

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return Response({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                load_yaml = Command()
                load_yaml.handle(stream)
                return Response({'Status': True})

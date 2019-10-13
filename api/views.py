from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import OrderShortSerializer, StateSerializer, OrderFullSerializer
from rest_framework import permissions

from app.models import Order


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


class PriceUpdateView(APIView):

    def post(self):
        pass
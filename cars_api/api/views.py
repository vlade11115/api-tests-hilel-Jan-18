import requests
from django.conf import settings
import django_filters.rest_framework
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Car, CarType, Order
from .serializers import CarSerializer, OrderSerializer


class CarList(generics.ListCreateAPIView):
    """
    List all cars.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['color', 'year', "car_type__brand", "car_type__price"]
    search_fields = ['color', "year", "car_type__brand"]
    ordering_fields = ["year", "car_type__price"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                car_type = CarType.objects.get(id=request.data["car_type"])
            except CarType.DoesNotExist:
                return Response({"error": "Car type not found"}, status=404)
            serializer.save(car_type=car_type)
            return Response({"car": serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class OrdersView(generics.ListCreateAPIView):
    """Create order"""
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        request_body = {"amount": 100}
        headers = {"X-Token": settings.MONOBANK_TOKEN}
        r = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=request_body, headers=headers)
        r.raise_for_status()
        serializer = OrderSerializer(data=dict(url=r.json()["pageUrl"], client=request.user.id))
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response({"order": serializer.data}, status=201)

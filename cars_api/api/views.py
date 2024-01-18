import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, CarType
from .serializers import CarSerializer, OrderSerializer


class CarList(APIView):
    """
    List all cars.
    """

    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response({"cars": serializer.data})

    def post(self, request, format=None):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            try:
                car_type = CarType.objects.get(id=request.data["car_type"])
            except CarType.DoesNotExist:
                return Response({"error": "Car type not found"}, status=404)
            serializer.save(car_type=car_type)
            return Response({"car": serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class Orders(APIView):
    """Create order"""

    def post(self, request, format=None):
        request_body = {"amount": 100}
        headers = {"X-Token": settings.MONOBANK_TOKEN}
        r = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=request_body, headers=headers)
        r.raise_for_status()
        serializer = OrderSerializer(dict(url=r.json()["pageUrl"]))
        return Response({"order": serializer.data}, status=201)

from rest_framework import serializers

from .models import Car, Order


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "year", "car_type", "color"]
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
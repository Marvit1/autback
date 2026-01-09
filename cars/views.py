from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Car, CarImage
from .serializers import CarSerializer, CarImageSerializer



class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def perform_create(self, serializer):
        car = serializer.save()
        # Handle multiple image uploads
        images_data = self.request.FILES.getlist('images')
        for image_data in images_data:
            CarImage.objects.create(car=car, image=image_data)

class CarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def perform_update(self, serializer):
        car = serializer.save()
        # Handle multiple image uploads on update
        images_data = self.request.FILES.getlist('images')
        for image_data in images_data:
            CarImage.objects.create(car=car, image=image_data)

class CarImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CarImageSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        car_id = self.kwargs['car_id']
        return CarImage.objects.filter(car_id=car_id)

    def perform_create(self, serializer):
        car = get_object_or_404(Car, id=self.kwargs['car_id'])
        # Ensure we don't exceed the 10-image limit
        if CarImage.objects.filter(car=car).count() >= 10:
            raise serializers.ValidationError("Maximum of 10 images per car allowed.")
        serializer.save(car=car)

class CarImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarImageSerializer
    lookup_url_kwarg = 'image_id'

    def get_queryset(self):
        car_id = self.kwargs['car_id']
        return CarImage.objects.filter(car_id=car_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs['image_id'])
        return obj
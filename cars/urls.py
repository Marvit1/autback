from django.urls import path
from .views import (
    CarListCreateAPIView, 
    CarDetailAPIView,
    CarImageListCreateAPIView,
    CarImageDetailAPIView
)

urlpatterns = [
    # Car endpoints
    path('cars/', CarListCreateAPIView.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarDetailAPIView.as_view(), name='car-detail'),
    
    # Car image endpoints
    path('cars/<int:car_id>/images/', CarImageListCreateAPIView.as_view(), name='car-image-list'),
    path('cars/<int:car_id>/images/<int:image_id>/', CarImageDetailAPIView.as_view(), name='car-image-detail'),
]
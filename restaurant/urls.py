from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import index, BookingCreateView

app_name = RestaurantConfig.name

urlpatterns = [
    path("", index, name='index'),
    path("booking_create/", BookingCreateView.as_view(), name='booking_create'),
]

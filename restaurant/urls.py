from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import index

app_name = RestaurantConfig

urlpatterns = [
    path("", index, name='index'),
]

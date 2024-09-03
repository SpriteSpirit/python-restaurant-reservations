from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import index

app_name = RestaurantConfig.name

urlpatterns = [
    path("", index, name='index'),
]

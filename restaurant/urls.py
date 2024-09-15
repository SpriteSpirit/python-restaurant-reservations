from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import TableListView, BookingCreateView

app_name = RestaurantConfig.name

urlpatterns = [
    path("", TableListView.as_view(), name='index'),
    path('booking/create/<int:table_id>/<str:date_reserved>/<str:time_reserved>/', BookingCreateView.as_view(),
         name='booking_create'),
]

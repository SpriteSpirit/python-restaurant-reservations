from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import TableListView, BookingCreateView, MainPageView, AboutPageView, MenuPageView, \
    GalleryPageView, BookingListView

app_name = RestaurantConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name='index'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("menu/", MenuPageView.as_view(), name='menu'),
    path("gallery/", GalleryPageView.as_view(), name='gallery'),

    # booking
    path("booking/", TableListView.as_view(), name='table_list'),
    path("booking_list/", BookingListView.as_view(), name='booking_list'),
    path('booking/create/<int:table_id>/<str:date_reserved>/<str:time_reserved>/', BookingCreateView.as_view(),
         name='booking_create'),
]

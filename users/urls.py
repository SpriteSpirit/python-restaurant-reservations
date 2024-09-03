from django.urls import path

from users.apps import UsersConfig
from users.views import user_list

app_name = UsersConfig

urlpatterns = [
    path("users/", user_list, name='users'),
]

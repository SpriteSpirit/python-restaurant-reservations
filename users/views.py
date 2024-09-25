from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm, CustomAuthenticationForm
from users.models import User


class UserRegisterView(CreateView):
    """
    Регистрация пользователя
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):
    """
    Авторизация пользователя
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('restaurant:index')


class UserDetailView(LoginView):
    """
    Просмотр профиля пользователя
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

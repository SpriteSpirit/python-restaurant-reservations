from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class StyleFormMixin:
    """
    Добавляет стилевые атрибуты к полям формы - стилизация формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователей с использованием стилей
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """
    Форма аутентификации пользователей с использованием стилей
    """
    class Meta:
        model = User
        fields = ('email', 'password')

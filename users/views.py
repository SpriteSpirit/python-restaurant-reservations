from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetCompleteView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from config import settings
from config.settings import EMAIL_HOST_USER
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


class ResetPasswordView(PasswordResetView):
    """
    Сброса пароля - переопределение класса PasswordResetView
    """
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('restaurant:index')
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        subject = 'Восстановление и сброс пароля'
        reset_link = self.request.build_absolute_uri(reverse('users:password_reset_confirm', args=[uid, token]))

        html_message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
            'site_name': 'MAILING SERVICE',
            'reset_link': reset_link,
        })

        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email=EMAIL_HOST_USER, recipient_list=[user.email],
                  html_message=html_message)

        return redirect(reverse('users:password_reset_done'))


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Подтверждение сброса пароля - переопределение класса PasswordResetConfirmView
    """
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class ResetPasswordCompleteView(PasswordResetCompleteView):
    """
    Завершение сброса пароля - переопределение класса PasswordResetCompleteView
    """
    template_name = "users/password_reset_complete.html"
    extra_context = {'title': _("Password reset complete")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context

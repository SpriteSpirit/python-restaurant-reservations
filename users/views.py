from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from users.forms import CustomAuthenticationForm


# class CustomLoginView(LoginView):
#     form_class = CustomAuthenticationForm
#     template_name = 'users/login.html'
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         user = self.request.user
#         print(f"Пользователь {user.email} вошел в аккаунт.")
#         return response
#
#     def get_success_url(self):
#         user = self.request.user
#
#         if user.is_authenticated and not (user.is_superuser or user.is_staff):
#             return reverse_lazy('restaurant:index')
#         # else:
#         #     return reverse_lazy('restaurant:moderator_dashboard')


# class CustomLogoutView(LogoutView):
#     form_class = CustomAuthenticationForm
#     template_name = 'users/logout.html'
#     next_page = reverse_lazy('restaurant:index')
#     # success_url = reverse_lazy('restaurant:index')

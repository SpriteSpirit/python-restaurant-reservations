from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from restaurant.forms import ChooseTableForm, BookingForm
from restaurant.models import Table, Booking, Restaurant
from users.models import User


class TableListView(ListView):
    model = Table
    template_name = 'restaurant/choose_table.html'
    context_object_name = 'tables'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # today = timezone.now().date()
        selected_date = None
        selected_time = None
        bookings = []
        table_statuses = []

        form = ChooseTableForm(self.request.POST or None)
        context['form'] = form

        if form.is_valid():
            selected_date = form.cleaned_data['date_reserved']
            selected_time = form.cleaned_data['time_reserved']
            bookings = Booking.objects.filter(date_reserved=selected_date, time_reserved=selected_time)

        booked_table_ids = [booking.table.id for booking in bookings]

        for table in context['tables']:
            booking = Booking.objects.filter(
                table=table,
                date_reserved=selected_date,
                time_reserved=selected_time
            ).first()

            if booking:
                table_status = {
                    'number': table.number,
                    'seats': table.seats,
                    'is_booked': table.id in booked_table_ids,
                    'date_reserved': booking.date_reserved,
                    'time_reserved': booking.time_reserved,
                }
            else:
                table_status = {
                    'number': table.number,
                    'seats': table.seats,
                    'is_booked': False,
                    'date_reserved': "-",
                    'time_reserved': "-",
                }

            table_statuses.append(table_status)

        context['table_statuses'] = table_statuses
        context['selected_date'] = selected_date
        context['selected_time'] = selected_time

        print("Дата:", selected_date)
        print("Время:", selected_time)
        print("Бронирования:", bookings)
        print("Статус столов:", table_statuses)

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class BookingCreateView(CreateView):
    """
    Бронирование
    """
    model = Booking
    form_class = BookingForm
    template_name = 'restaurant/booking_form.html'
    success_url = reverse_lazy('restaurant:index')

    def get_initial(self):
        """
         Получение начальных данных для формы заказа.
         Если переданы id стола, дата и время бронирования,
         присваивание текущего пользователя заказу и стола.
        """
        initial = super().get_initial()
        table_id = self.kwargs.get('table_id')
        date_reserved = self.kwargs.get('date_reserved')
        time_reserved = self.kwargs.get('time_reserved')
        user_id = self.request.user.pk

        if table_id and date_reserved and time_reserved:
            initial['client'] = User.objects.get(pk=user_id)
            initial['table'] = Table.objects.get(id=table_id)
            initial['seats'] = Table.objects.get(id=table_id).seats
            initial['date_reserved'] = date_reserved
            initial['time_reserved'] = time_reserved

        return initial

    def form_valid(self, form):
        """
         Переопределение формы валидации.
         Присваивание текущего пользователя к заказу.
         Логирование данные перед сохранением.
        """
        booking = form.save(commit=False)
        booking.client = self.request.user

        print(f"Дата бронирования: {booking.date_reserved}")
        print(f"Время бронирования: {booking.time_reserved}")
        print(f"Стол: {booking.table}")
        print(f"Клиент: {booking.client}")

        booking.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        """
         Вывод ошибки формы
        """
        print("Форма не прошла валидацию. Ошибки:", form.errors)
        return super().form_invalid(form)


class BookingListView(ListView):
    """
    Просмотр списка бронирований
    """
    model = Booking
    context_object_name = 'bookings'

    def get_queryset(self):
        """ Просмотр только своих бронирований """
        user = self.request.user
        return Booking.objects.filter(client=user)


class MainPageView(TemplateView):
    """
    Главная страница ресторана.
    """
    model = Restaurant
    template_name = 'restaurant/index.html'


class AboutPageView(TemplateView):
    """
    Страница с информацией о ресторане.
    """
    model = Restaurant
    template_name = 'restaurant/about.html'


class MenuPageView(TemplateView):
    """
    Страница с меню.
    """
    model = Restaurant
    template_name = 'restaurant/menu.html'


class GalleryPageView(TemplateView):
    """
    Галерея.
    """
    model = Restaurant
    template_name = 'restaurant/gallery.html'

# TODO: ЛК: просмотр истории бронирования
# TODO: ЛК: управление текущими бронированиями (изменение, отмена)
# TODO: Админка:Управление пользователями
# TODO: Админка:Управление бронированиями
# TODO: Управление контентом сайта (тексты, изображения и т.д.)

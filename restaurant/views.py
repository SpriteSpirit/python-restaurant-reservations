from django.utils import timezone
from django.views.generic import CreateView, ListView

from restaurant.forms import ChooseTableForm, BookingForm
from restaurant.models import Table, Booking


class TableListView(ListView):
    model = Table
    template_name = 'restaurant/choose_table.html'
    context_object_name = 'tables'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        selected_date = None
        selected_time= None
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
            booking = Booking.objects.filter(table=table, date_reserved=selected_date, time_reserved=selected_time).first()

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
    View для создания бронирования.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'restaurant/booking_form.html'
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.kwargs.get('table_id')
        date_reserved = self.kwargs.get('date_reserved')
        time_reserved = self.kwargs.get('time_reserved')

        if table_id and date_reserved and time_reserved:
            initial['table'] = Table.objects.get(id=table_id)
            initial['seats'] = Table.objects.get(id=table_id).seats
            initial['date_reserved'] = date_reserved
            initial['time_reserved'] = time_reserved

        return initial

    def form_valid(self, form):
        self.object = form.save()

        if form.is_valid():
            booking = form.save(commit=False)
            print("Бронирование прошло успешно!")
            print(f"Стол: {self.object.table}")
            print(f"Дата бронирования: {self.object.date_reserved}")
            print(f"Время бронирования: {self.object.time_reserved}")
            booking.save()

        return super().form_valid(form)

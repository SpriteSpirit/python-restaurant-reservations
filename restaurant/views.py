from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView

from restaurant.forms import ChooseTableForm
from restaurant.models import Table, Booking


# TODO : изменить функцию на класс BookingListView
# TODO : создать форму для бронирования booking_form.py


def index(request):
    today = timezone.now().date()
    tables = Table.objects.all()
    selected_date = None
    bookings = []
    table_statuses = []

    if request.method == "POST":
        form = ChooseTableForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date_reserved']
            # Получаем все бронирования на выбранную дату
            bookings = Booking.objects.filter(date_reserved=selected_date)
    else:
        form = ChooseTableForm()

    booked_table_ids = [booking.table.id for booking in bookings]

    for table in tables:
        # Получаем первое бронирование для стола на выбранную дату, если оно есть
        booking = Booking.objects.filter(table=table, date_reserved=selected_date).first()

        if booking:
            table_status = {
                'number': table.number,
                'capacity': table.capacity,
                'is_booked': table.id in booked_table_ids,
                'date_reserved': booking.date_reserved,
                'time_reserved': booking.time_reserved,
            }
        else:
            table_status = {
                'number': table.number,
                'capacity': table.capacity,
                'is_booked': False,
                'date_reserved': "-",
                'time_reserved': "-",
            }

        table_statuses.append(table_status)

    print(table_statuses)

    context = {
        'form': form,
        'table_statuses': table_statuses,
        'selected_date': selected_date,
        'today': today,
    }

    print("Selected date:", selected_date)
    print("Bookings:", bookings)
    print("Table statuses:", table_statuses)

    return render(request, 'restaurant/choose_table.html', context)


class BookingCreateView(CreateView):
    """
    View для создания бронирования.
    """
    model = Booking
    form_class = ChooseTableForm
    template_name = 'restaurant/booking_form.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()

        if form.is_valid():
            booking = form.save(commit=False)
            print("Booking created successfully!")
            print(f"Table: {self.object.table}")
            print(f"Date reserved: {self.object.date_reserved}")
            print(f"Time reserved: {self.object.time_reserved}")
            booking.save()

        return super().form_valid(form)

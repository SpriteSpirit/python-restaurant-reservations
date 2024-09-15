from django import forms
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Booking


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ChooseTableForm(StyleFormMixin, forms.ModelForm):
    open_time = 10
    close_booking_time = 20
    time_step = 30

    time_reserved = forms.ChoiceField(label='Время бронирования')

    next_day = timezone.localdate() + timedelta(days=1)

    date_reserved = forms.DateField(
        label="Дата бронирования",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': next_day.strftime('%Y-%m-%d'),
            'max': (next_day + timedelta(days=6)).strftime('%Y-%m-%d'),
        }),
    )

    def __init__(self, *args, **kwargs):
        super(ChooseTableForm, self).__init__(*args, **kwargs)

        times = [
            (datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time(), f"{hour:02d}:{minute:02d}")
            for hour in range(self.open_time, self.close_booking_time + 1) for minute in [0, self.time_step]
            if hour < self.close_booking_time or (hour == self.close_booking_time and minute == 0)
        ]

        self.fields['time_reserved'].choices = times

    class Meta:
        model = Booking
        fields = ['date_reserved']

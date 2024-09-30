from django import forms
from django.utils import timezone
from datetime import timedelta, datetime

from users.models import User
from .models import Booking, Table


class StyleFormMixin:
    """
    Добавляет стилевые атрибуты к полям формы - стилизация формы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ChooseTableForm(StyleFormMixin, forms.ModelForm):
    """
    Форма выбора стола с поддержкой временных интервалов бронирования
    """
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
        fields = ['date_reserved', 'time_reserved']


class BookingForm(StyleFormMixin, forms.ModelForm):
    """
    Форма бронирования с использованием стилей
    """
    seats = forms.IntegerField(label='Количество мест', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    table = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'initial' in kwargs and kwargs['initial']:
            initial_data = kwargs['initial']

            if 'seats' in initial_data:
                self.fields['seats'].initial = initial_data['seats']
            if 'table' in initial_data:
                self.initial['table'] = initial_data['table']
                self.fields['table'].widget.attrs['value'] = self.initial['table'].id
    #

    class Meta:
        model = Booking
        fields = ['table', 'seats', 'date_reserved', 'time_reserved', 'message']
        widgets = {
            'table': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'seats': forms.TextInput(attrs={'readonly': 'readonly'}),
            'date_reserved': forms.DateInput(attrs={'readonly': 'readonly'}),
            'time_reserved': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'message': forms.Textarea(attrs={'placeholder': 'Дополнительная информация'}),
        }

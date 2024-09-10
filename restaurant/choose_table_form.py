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


class BookingForm(StyleFormMixin, forms.ModelForm):
    time_reserved = forms.ChoiceField(label='Время бронирования')

    # Настройка виджета для выбора даты с ограничением по min и max
    date_reserved = forms.DateField(
        label="Дата бронирования",
        widget=forms.DateInput(attrs={
            'type': 'date',  # HTML5 date input
            'min': timezone.now().date().strftime('%Y-%m-%d'),  # Минимальная дата - сегодня
            'max': (timezone.now().date() + timedelta(days=7)).strftime('%Y-%m-%d'),  # Максимум через 7 дней
        }),
    )

    class Meta:
        model = Booking
        fields = ['date_reserved']  # Поля формы

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Генерируем выбор времени с шагом 30 минут
        times = [(datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time(), f"{hour:02d}:{minute:02d}")
                 for hour in range(10, 21) for minute in [0, 30]]
        self.fields['time_reserved'].choices = times

    def clean_date_reserved(self):
        date_reserved = self.cleaned_data['date_reserved']
        today = timezone.now().date()
        max_date = today + timedelta(days=7)

        if date_reserved < today:
            raise forms.ValidationError("Нельзя выбрать дату в прошлом.")
        if date_reserved > max_date:
            raise forms.ValidationError(f"Дата бронирования не может быть позже {max_date}.")

        return date_reserved

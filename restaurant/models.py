from datetime import datetime

from django.db import models
# from datetime import datetime, timedelta
# default=datetime.now().time() + timedelta(hours=3)
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Restaurant(models.Model):
    """ Ресторан """
    objects = models.Manager()

    name = models.CharField(max_length=255, verbose_name="Название ресторана")
    address = models.CharField(max_length=255, verbose_name="Адрес ресторана")
    phone_number = PhoneNumberField(default='+7', verbose_name="Номер телефона")

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'
        ordering = ('name',)

    def __str__(self):
        return f'Ресторан: {self.name}'


class Table(models.Model):
    """ Стол """

    objects = models.Manager()

    number = models.IntegerField(verbose_name="Номер стола")
    capacity = models.IntegerField(verbose_name="Количество человек на стол")
    is_booked = models.BooleanField(verbose_name="Забронирован", default=False)
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name='tables',
                                   verbose_name='Ресторан',
                                   default=1)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'Стол {self.number} в ресторане {self.restaurant.name}'


class Booking(models.Model):
    """ Бронирование стола """
    objects = models.Manager()

    table = models.ForeignKey(Table,
                              on_delete=models.SET_NULL,
                              related_name='bookings',
                              verbose_name='Стол',
                              **NULLABLE)
    client = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               related_name='bookings',
                               verbose_name="Клиент",
                               **NULLABLE)
    date_reserved = models.DateField(verbose_name="Дата бронирования")
    time_reserved = models.TimeField(verbose_name="Время бронирования")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность бронирования", default=3)  # в часах
    is_active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Бронирование стола {self.table.number} на {self.date_reserved} в {self.time_reserved}'

    @property
    def end_time(self):
        """
        Возвращает время окончания бронирования на основе времени начала и продолжительности.
        """
        start_datetime = datetime.combine(self.date_reserved, self.time_reserved)
        end_datetime = start_datetime + self.duration
        return end_datetime.time()  # Возвращаем только время


from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Restaurant(models.Model):
    """
    Ресторан
    """
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
    """
    Стол
    """

    objects = models.Manager()

    number = models.IntegerField(verbose_name="Номер стола")
    seats = models.IntegerField(verbose_name="Количество человек на стол")
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


class AbstractBooking(models.Model):
    """
    Абстрактная базовая модель для бронирований.
    """
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, related_name='%(class)ss', verbose_name='Стол', **NULLABLE)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)ss', verbose_name="Клиент", **NULLABLE)
    date_reserved = models.DateField(verbose_name="Дата бронирования")
    time_reserved = models.TimeField(verbose_name="Время бронирования")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность бронирования", default=3)
    message = models.TextField(verbose_name="Сообщение",  **NULLABLE)

    class Meta:
        abstract = True

    def __str__(self):
        table_number = self.table.number if self.table else 'Неизвестный стол'
        return f'Бронирование стола {table_number} на {self.date_reserved} в {self.time_reserved}'


class Booking(AbstractBooking):
    """
    Бронирование стола
    """
    is_active = models.BooleanField(verbose_name="Активно", default=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def cancel(self):
        """
        Отмена бронирования
        """
        BookingHistory.objects.create(
            table=self.table,
            client=self.client,
            date_reserved=self.date_reserved,
            time_reserved=self.time_reserved,
            duration=self.duration,
            message=self.message,
            cancelled_at=timezone.now()
        )

        if self.table:
            self.table.is_booked = False
            self.table.save()

        self.delete()


class BookingHistory(AbstractBooking):
    """
    История бронирования
    """
    cancelled_at = models.DateTimeField(verbose_name="Время отмены бронирования")
    objects = models.Manager()

    class Meta:
        verbose_name = 'История бронирования'
        verbose_name_plural = 'История бронирований'

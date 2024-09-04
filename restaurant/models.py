from django.db import models


class Table(models.Model):
    number = models.IntegerField(verbose_name="Номер стола")
    capacity = models.IntegerField(verbose_name="Количество человек на стол")
    is_booked = models.BooleanField(verbose_name="Забронирован", default=False)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'Стол {self.number}'

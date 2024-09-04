from django.contrib import admin
from restaurant.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity', 'number', 'is_booked')
    list_filter = ('capacity', 'is_booked', 'number')
    # search_fields = ('restaurant__name', 'number'
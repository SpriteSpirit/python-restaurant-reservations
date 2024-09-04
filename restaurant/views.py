from django.shortcuts import render

from restaurant.models import Table


def index(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/book_table.html', context)

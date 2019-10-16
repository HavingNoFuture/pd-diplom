from django.template import Library
from django.db.models import Min

register = Library()


@register.filter()
def min_price(queryset):
    min = queryset.aggregate(Min('price'))["price__min"]
    if min is None:
        return 'Товар отсутствует'
    return f'Цена от: {min} руб.'


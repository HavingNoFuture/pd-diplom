from django.template import Library
from django.db.models import Min

register = Library()


@register.filter()
def min_price(queryset):
    min = queryset.aggregate(Min('price'))
    return min['price__min']


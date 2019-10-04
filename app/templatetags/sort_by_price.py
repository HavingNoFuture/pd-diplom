from django.template import Library

register = Library()


@register.filter()
def sort_by_price(queryset):
    sorted_qs = queryset.order_by('price')
    return sorted_qs
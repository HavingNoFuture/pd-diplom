from django.template import Library


register = Library()


@register.filter()
def default_value(value, token):
    value.field.widget.attrs["value"] = token
    return value


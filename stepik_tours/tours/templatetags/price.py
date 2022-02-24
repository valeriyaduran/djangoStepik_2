from django import template

register = template.Library()


@register.filter()
def price(value):
    price = int(value)
    return '{:,}'.format(price).replace(',', ' ')

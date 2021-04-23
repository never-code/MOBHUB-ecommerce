from django import template
from store.models import Product

register = template.Library()


@register.inclusion_tag('store/similar.html')
def get_similar(id, price, category, count=5):
    min_p = price - (0.25*price)
    max_p = price + (0.25*price)
    products = Product.objects.filter(
        category=category, price__gte=min_p, price__lte=max_p).exclude(pk=id)[:count]
    return {'products': products}


@register.filter
def getattr(obj, arg):
    return obj[str(arg)]

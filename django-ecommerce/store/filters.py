import django_filters
from store.models import Category, Product


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', widget=django_filters.widgets.forms.HiddenInput())

    class Meta:
        model = Product
        fields = ('name', 'category', 'price')

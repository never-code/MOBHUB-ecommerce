from django.db import models
from django.conf import settings
from store.models import Product
from django.shortcuts import reverse

# Create your models here.

choices = (
    ('Pending', 'Pending'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered')
)
PAYMENT = (
    ('COD', 'COD'),
    ('PayTm', 'PayTm'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='orders', on_delete=models.CASCADE)
    address = models.CharField(max_length=150, blank=False, null=False)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    Phone = models.CharField(max_length = 10, default = ' ')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=choices, max_length=10, default='Pending')
    payment=models.CharField(choices=PAYMENT,max_length=10,default='COD')
    total_price = models.FloatField(null=False, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_absolute_url(self):
        return reverse('orders:invoice', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='ordered', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'Order Item {self.id}'

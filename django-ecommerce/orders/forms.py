from orders.models import Order
from django import forms

PAYMENT_CHOICES = (
    ('COD', 'Cash on Delivery'),
    ('P', 'PayTm'),
    ('S', 'Stripe'),
)

class CheckoutFormPaymentOption(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=PAYMENT_CHOICES)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'city', 'pin_code','payment', 'Phone']

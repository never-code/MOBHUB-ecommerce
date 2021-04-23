from django import forms


class CartForm(forms.Form):
    product_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, required=True, widget=forms.NumberInput({'class': 'form-control', 'value': 1}))

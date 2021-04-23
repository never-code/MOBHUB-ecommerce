from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from store.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from cart.forms import CartForm
# Create your views here.


@login_required
@require_POST
def add_to_cart(request):
    cart = Cart(request)
    form = CartForm(request.POST)
    if form.is_valid():
        product_id = form.cleaned_data['product_id']
        quantity = form.cleaned_data['quantity']
        product = get_object_or_404(Product, id=product_id, availibility=True)
        cart.add(product_id, product.price, quantity)
        messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:cart_details')


@login_required
def cart_details(request):
    cart = Cart(request)
    products = Product.objects.filter(pk__in=cart.cart.keys())

    def map_function(p):
        pid = str(p.id)
        q = cart.cart[pid]['quantity']
        return {'product': p, 'quantity': q, 'total': p.price*q, 'form': CartForm(initial={'quantity': q, 'product_id': pid})}

    cart_items = map(map_function, products)
    return render(request, 'cart/cart_details.html', {'cart_items': cart_items, 'total': cart.get_total_price()})


@login_required
def remove_from_cart(request, id):
    cart = Cart(request)
    cart.remove(str(id))
    return redirect('cart:cart_details')


@login_required
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_details')

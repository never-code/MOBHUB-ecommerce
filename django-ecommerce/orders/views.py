from django.shortcuts import render, redirect, Http404
from django.views import generic
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from cart.cart import Cart
from django.db.models import Count
from store.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CreateOrder(LoginRequiredMixin, generic.CreateView):
    form_class = OrderForm
    template_name = 'orders/place_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        products = Product.objects.filter(pk__in=cart.cart.keys())
        cart_items = map(
            lambda p: {'product': p, 'quantity': cart.cart[str(p.id)]['quantity'], 'total': p.price*cart.cart[str(p.id)]['quantity']}, products)
        context['summary'] = cart_items
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        if len(cart) == 0:
            return redirect('cart:cart_details')
        order = form.save(commit=False)
        order.user = self.request.user
        order.total_price = cart.get_total_price()
        order.save()
        products = Product.objects.filter(id__in=cart.cart.keys())
        orderitems = []
        for i in products:
            q = cart.cart[str(i.id)]['quantity']
            orderitems.append(
                OrderItem(order=order, product=i, quantity=q, total=q*i.price))
        OrderItem.objects.bulk_create(orderitems)
        cart.clear()
        messages.success(self.request, 'Your order is successfully placed.')
        return redirect('store:product_list')


class MyOrders(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).annotate(total_items=Count('items'))


class OrderDetails(LoginRequiredMixin, generic.DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_details.html'

    def get_queryset(self, **kwargs):
        objs = super().get_queryset(**kwargs)
        return objs.filter(user=self.request.user).prefetch_related('items', 'items__product')


class OrderInvoice(LoginRequiredMixin, generic.DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_invoice.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('items', 'items__product')

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        if obj.user_id == self.request.user.id or self.request.user.is_superuser:
            return obj
        raise Http404

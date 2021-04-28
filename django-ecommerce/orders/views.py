from django.shortcuts import render, redirect, Http404
from django.views import generic
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from cart.cart import Cart
from django.db.models import Count
from store.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from Paytm import Checksum
# Create your views here.


MERCHANT_KEY = '15Oo@vdvanPfefG!'

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
        form_payment=form.cleaned_data['payment']
        order.user = self.request.user
        order.total_price = cart.get_total_price()
        order.save()
        if form_payment=="COD":
            print(form_payment)
        elif form_payment=='PayTm':
            orderid = order.id
            order.save()
            param_dict = {
                'MID': 'XouRsh60629205732669',
                'ORDER_ID': str(orderid),
                'TXN_AMOUNT': str(order.total_price),
                'CUST_ID': self.request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': f'http://127.0.0.1:8000/course/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(self.request, 'orders/paytm.html', {'param_dict': param_dict})        # else:

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

# @csrf_exempt
def handlerequest(request,course_slug,username):
    user=Account.objects.get(username=username)
    for _ in range(10):
        print("hello")
        print(user.email)
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            course = Course.objects.get(slug=course_slug)
            # user=request.user
            name = 'name'
            email = user.email
            mobile = user.phone_number
            amount = float(course.price)
            # order = Transaction.objects.create(user=user, item_json=course.name, course=course, name=name,
            #                                    email=email, mobile=mobile, amount=float(amount))
            order.save()
            course.member.add(user)
            course.save()
            messages.success(request,"Course is successfully purchase")
            return redirect("purchase_course")
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')
            # print('order successful')

        else:
            messages.error(request, "Something Went Wrong")
            return redirect("checkout",course_slug)
            # print('Something went wrong' + response_dict['RESPMSG'])
    return render(request, 'paytm/paytm_payment_status.html', {'response_dict': response_dict})




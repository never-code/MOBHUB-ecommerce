from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('place', views.CreateOrder.as_view(), name='place'),
    path('my', views.MyOrders.as_view(), name='my'),
    path('details/<int:pk>/', views.OrderDetails.as_view(), name='details'),
    path('invoice/<int:pk>/', views.OrderInvoice.as_view(), name='invoice')
]

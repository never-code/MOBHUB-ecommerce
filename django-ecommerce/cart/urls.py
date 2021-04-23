from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_details, name="cart_details"),
    path('add', views.add_to_cart, name="add"),
    path('remove/<int:id>', views.remove_from_cart, name="remove"),
    path('clear/', views.clear_cart, name="clear")
]

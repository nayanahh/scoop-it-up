from . import views
from django.urls import path

urlpatterns = [
    path('', views.orders_view, name='orders'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('checkout/', views.checkout, name='checkout'),
]
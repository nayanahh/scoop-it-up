from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.conf import settings
from .models import Cart, CartItem, Order, OrderItem
from menu.models import Food

import razorpay

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'orders.html', context)

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price for item in items)
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, food=food, defaults={'quantity': 1})
    if not item_created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{food.name} added to cart.")
    return redirect('home')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', item.quantity))
        
        if action == 'increase':
            quantity = item.quantity + 1
        elif action == 'decrease':
            quantity = item.quantity - 1
        
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, f"Quantity updated to {quantity}.")
        else:
            item.delete()
            messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
    
    total = sum(item.total_price for item in items)
    
    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(user=request.user, total_amount=total)
        
        # Create order items from cart items
        for item in items:
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('orders')
    
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'checkout.html', context)


@login_required
@require_POST
def create_razorpay_order(request):
    # Create a Razorpay order for the current user's cart and return order details
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        if not items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        total = sum(item.total_price for item in items)
        amount_paise = int(total * 100)  # Razorpay expects amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # Receipt id
        import time
        receipt = f"order_rcpt_{request.user.id}_{int(time.time())}"

        data = {
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': receipt,
            'payment_capture': 1
        }
        rzp_order = client.order.create(data=data)

        return JsonResponse({
            'order_id': rzp_order.get('id'),
            'amount': rzp_order.get('amount'),
            'currency': rzp_order.get('currency'),
            'key': settings.RAZORPAY_KEY_ID,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

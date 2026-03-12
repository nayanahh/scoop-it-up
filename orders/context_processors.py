from .models import Cart
from django.conf import settings

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items.count()
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0
    return {
        'cart_item_count': count,
        'MEDIA_URL': settings.MEDIA_URL,
    }
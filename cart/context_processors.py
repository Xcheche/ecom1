from cart.models import Cart, CartItem
from cart.views import _cart_id


def counter(request):
    """
    Context processor to provide cart_count, cart_items, and grand_total
    for dropdown on all pages.
    """
    if "admin" in request.path:
        return {}

    cart_count = 0
    cart_items = []
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            cart_count += item.quantity
            grand_total += item.product.current_price * item.quantity

    except Cart.DoesNotExist:
        pass

    return {
        "cart_count": cart_count,
        "cart_items": cart_items,
        "grand_total": grand_total,
    }


# from cart.models import Cart, CartItem
# from cart.views import _cart_id


# def counter(request):
#     """
#     A context processor to provide cart count and cart items globally.
#     """
#     # Skip admin
#     if "admin" in request.path:
#         return {}

#     cart_count = 0
#     cart_items = []

#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)

#         for item in cart_items:
#             cart_count += item.quantity

#     except Cart.DoesNotExist:
#         cart_count = 0
#         cart_items = []

#     return {
#         "cart_count": cart_count,
#         "cart_items": cart_items,
#     }

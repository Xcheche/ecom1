"""Context processors for the ``cart`` application.

A context processor is a callable that receives an :class:`HttpRequest`
and returns a ``dict`` merged into every rendered template's context.
Registering these processors in ``settings.TEMPLATES`` makes cart data
(mini-cart count, line items, grand total) available on every page —
including pages served by other apps — without having to thread it
through every view.
"""

from cart.models import Cart, CartItem
from cart.views import _cart_id


def counter(request):
    """Inject cart-summary variables into every template's context.

    Skips processing for the Django admin to avoid opening a cart per
    admin request and to keep the admin UI snappy. For all other paths we
    load the visitor's :class:`Cart` (creating nothing — if no cart exists
    we simply expose empty defaults), aggregate the line items, and
    return the totals for the header mini-cart widget.

    Args:
        request (HttpRequest): The incoming request being processed.

    Returns:
        dict: A mapping containing the keys ``cart_count``, ``cart_items``
        and ``grand_total``. Empty dict for admin paths.
    """
    if "admin" in request.path:
        # Don't run cart queries for the admin site — keep the UI fast and
        # avoid creating stray sessions for staff users.
        return {}

    cart_count = 0
    cart_items = []
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            cart_count += item.quantity
            grand_total += item.product.price * item.quantity

    except Cart.DoesNotExist:
        # No cart yet for this session — expose zeroed defaults so the
        # template can render an empty mini-cart without conditional noise.
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

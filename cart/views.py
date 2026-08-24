"""View layer for the ``cart`` application.

The cart is keyed to the visitor's Django session (see :func:`_cart_id`) and
backed by two relational tables:

* :class:`cart.models.Cart`       - one row per anonymous session.
* :class:`cart.models.CartItem`   - line items (product + quantity).

Exposed endpoints:

* :func:`add_cart`          - add a unit of a product to the cart.
* :func:`decrease_cart`     - remove a unit (or delete the line at 1).
* :func:`remove_cart_item`  - hard-delete a line item.
* :func:`cart`              - render the cart page with totals and tax.

All monetary math is performed with :class:`decimal.Decimal` to avoid the
floating-point rounding issues that ``float`` introduces on totals.
"""

from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product

from .models import Cart, CartItem


# Create your views here.
# =============================================================
# ======================Cart Session ID========================
# =============================================================
def _cart_id(request):
    """Return a stable identifier for the visitor's cart.

    We piggyback on Django's session framework: the session key is reused if
    it exists, otherwise a fresh session is created and persisted.

    Args:
        request (HttpRequest): The incoming request whose session is used.

    Returns:
        str: The session key bound to the visitor's cart row.
    """
    """We get the session id from the request"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.save()
    return cart


# =============================================================
# ======================Add Cart ========================
# =============================================================
def add_cart(request, product_id):
    """Add one unit of ``product_id`` to the visitor's cart.

    Behaviour:
        * If no cart exists for the current session, create one.
        * If the product is already in the cart, increment its quantity.
        * Otherwise create a new :class:`CartItem` with quantity ``1``.

    On success we redirect the user back to where they came from (e.g. the
    PDP), falling back to the cart page if ``HTTP_REFERER`` is unavailable.

    Args:
        request (HttpRequest): Incoming request.
        product_id (int): PK of the :class:`store.models.Product` to add.
    """
    """Adding cart items to the cart"""
    product = Product.objects.get(id=product_id)  # Get the product
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # Get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # Increment the quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
        # for debugging purpose
    # return HttpResponse(cart_item.quantity)
    # return HttpResponse(cart_item.id)
    # return HttpResponse(cart_item.product_name)
    # exit()
    return redirect(request.META.get("HTTP_REFERER", "cart:cart"))


# =============================================================
# ======================Decrease Cart ========================
# =============================================================
def decrease_cart(request, product_id):
    """Remove one unit of ``product_id`` from the visitor's cart.

    When the existing quantity is greater than one we decrement; once it
    reaches one we delete the line entirely to avoid zero-quantity rows.

    Args:
        request (HttpRequest): Incoming request.
        product_id (int): PK of the :class:`store.models.Product` to decrement.
    """
    """Removing cart items from the cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass
    except CartItem.DoesNotExist:
        pass

    return redirect(request.META.get("HTTP_REFERER", "cart:cart"))


# =============================================================
# ======================Remove Cart Item ========================
# =============================================================
def remove_cart_item(request, product_id):
    """Hard-delete the cart line item for ``product_id``.

    Unlike :func:`decrease_cart` this does not look at the current quantity —
    the row is removed unconditionally.

    Args:
        request (HttpRequest): Incoming request.
        product_id (int): PK of the :class:`store.models.Product` to remove.
    """
    """Completely removing a particular cart item from the cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect("cart:cart")


# =============================================================
# ======================Cart Details========================
# =============================================================
def cart(request, total=Decimal("0.00"), quantity=0, cart_items=None):
    """Render the cart page with totals, taxes and line items.

    Iterates over every active :class:`CartItem` for the visitor's cart,
    accumulating a running subtotal and item count, then applies a flat
    tax rate (industry-standard pattern: keep rates in one place; here we
    hard-code 7.5% for demonstration).

    Args:
        request (HttpRequest): Incoming request.
        total (Decimal): Running subtotal of line items (default ``0.00``).
        quantity (int):   Running count of items across all lines.
        cart_items (list[CartItem] | None): Reused buffer; rebuilt below.

    Context:
        total (Decimal):     Subtotal before tax.
        quantity (int):      Total units across all line items.
        cart_items (list):   Active line items for the visitor.
        tax (Decimal):       Computed tax for the subtotal.
        grand_total (Decimal): ``total + tax``.
    """
    tax = Decimal("0.00")
    grand_total = Decimal("0.00")
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax_rate = Decimal("0.075")  # 7.5%
        tax = total * tax_rate
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "cart/cart.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from decimal import Decimal

from store.models import Product
from .models import Cart, CartItem

# Create your views here.

# ------------------- Cart session --------------------


def _cart_id(request):
    """We get the session id from the request"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.save()
    return cart


# -------------------Adding cart view --------------------


def add_cart(request, product_id):
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


#-------------------Decrease cart view --------------------
def decrease_cart(request, product_id):
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


#-----------------------Remove_particular_item--------------------
def remove_cart_item(request, product_id):
    """Completely removing a particular cart item from the cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    
    return redirect("cart:cart")

# -------------------Cart view --------------------
# def cart(request, total=0, quantity=0, cart_items=None):
#     """
#     This function retrieves the cart items for a user and calculates the total price and quantity.
#     """

#     #  initialize first
#     tax = 0
#     grand_total = 0
#     cart_items = []
#     try:
#         # Getting the cart using the cart_id from the session _means is private function
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         # Calculating the total price and quantity of the cart items
#         for cart_item in cart_items:
#             total += cart_item.product.price * cart_item.quantity
#             quantity += cart_item.quantity
#         # Tax    choose according to location tax rate or vat
#         tax = (0.075 * total) / 100
#         grand_total = total + tax
#     except Exception:
#         pass  # just ignore

#     context = {
#         "total": total,
#         "quantity": quantity,
#         "cart_items": cart_items,
#         "tax": tax,
#         "grand_total": grand_total,
#     }
#     return render(request, "cart/cart.html", context)




def cart(request, total=Decimal("0.00"), quantity=0, cart_items=None):
    tax = Decimal("0.00")
    grand_total = Decimal("0.00")
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += item.product.current_price * item.quantity
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

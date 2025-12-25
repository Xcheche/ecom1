from django.shortcuts import get_object_or_404, render

from store.models import Category, Product
from cart.models import Cart, CartItem
from cart.views import _cart_id  # or wherever it lives


# Create your views here.


def store(request):
    try:
        products = Product.objects.all().filter(is_available=True)
    except Exception:
        # Handle the case where products are not found
        return render(request, "404.html", status=404)
    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)


# Category view
# Store view with optional category filtering
def category_view(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        category = None
        products = Product.objects.filter(is_available=True)

    product_count = products.count()

    context = {
        "category": category,
        "products": products,
        "product_count": product_count,
        # 'links' will come from your context processor automatically
    }

    return render(request, "store/index.html", context)


# def product_detail(request, category_slug, product_slug):
#     try:
#         category = get_object_or_404(Category, slug=category_slug)
#         product = get_object_or_404(
#             Product, slug=product_slug, category=category, is_available=True
#         )
#     except Exception as e:
#         # Handle the case where the category or product is not found
#         raise e
#     context = {
#         "product": product,
#         "category": category,
#     }
#     return render(request, "store/detail.html", context)


def product_detail(request, category_slug, product_slug):
    in_cart = False
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product, slug=product_slug, category=category, is_available=True
    )
    #Check if in cart
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
     # Get cart quantity

    cart_qty = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_qty = cart_item.quantity
    except Cart.DoesNotExist:
        pass
    except CartItem.DoesNotExist:
        pass

    context = {
        "product": product,
        "category": category,
        "cart_qty": cart_qty,  # ✅ THIS IS THE KEY
        "in_cart": in_cart,
    }
    return render(request, "store/detail.html", context)
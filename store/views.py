"""View layer for the ``store`` application.

The storefront exposes three read-only endpoints:

* :func:`store`            - the homepage / catalog landing page.
* :func:`category_view`    - catalog filtered by a single category slug.
* :func:`product_detail`   - product detail page (PDP).

The cart-aware bits on the PDP rely on :func:`cart.views._cart_id` to
associate the anonymous visitor's session with a persistent ``Cart`` row and
its ``CartItem`` children. This keeps the cart working for both authenticated
and anonymous users.
"""

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from store.models import Category, Product
from cart.models import Cart, CartItem
from cart.views import _cart_id  # or wherever it lives


# Create your views here.


def paginate_products(request, queryset, per_page=3):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")
    return paginator.get_page(page)


# =============================================================
# ======================Store View========================
# =============================================================
def store(request):
    """Render the storefront homepage with all available products.

    Fetches every :class:`store.models.Product` whose ``is_available`` flag is
    ``True``. If the lookup fails for any reason (e.g. database is not yet
    migrated), we fall back to a 404 page rather than letting the request
    blow up with a 500.

    Context:
        products (QuerySet[Product]): Visible products shown in the catalog.

    Returns:
        HttpResponse: The rendered ``store/index.html`` template.
    """
    print("store view called")
    try:
        # products = Product.objects.all().filter(is_available=True)
        products = Product.objects.filter(is_available=True)
        products = paginate_products(request, products)
    except Exception:
        # Handle the case where products are not found
        return render(request, "404.html", status=404)
    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)


# =============================================================
# ======================Category View========================
# =============================================================
# def category_view(request, category_slug=None):
#     """Render the catalog filtered by a single category.

#     When ``category_slug`` is supplied we narrow the product queryset to that
#     category; otherwise we fall back to the full available catalog. The view
#     also computes a ``product_count`` used in the sidebar widget.

#     Context:
#         category (Category | None):  The matched category, or ``None`` when
#                                     browsing the full catalog.
#         products (QuerySet[Product]): Products to display.
#         product_count (int):         Number of products in ``products``.
#     """
#     print("category view called")
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(category=category, is_available=True)
#         products = paginate_products(request, products)
#     else:
#         category = None
#         products = Product.objects.filter(is_available=True)
#         products = paginate_products(request, products)

#     product_count = products.count()

#     context = {
#         "category": category,
#         "products": products,
#         "product_count": product_count,
#         # 'links' will come from your context processor automatically
#     }

#     return render(request, "store/index.html", context)
def category_view(request, category_slug=None):
    print("category view called")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category,
            is_available=True
        )
    else:
        category = None
        products = Product.objects.filter(is_available=True)

    product_count = products.count()
    products = paginate_products(request, products)

    context = {
        "category": category,
        "products": products,
        "product_count": product_count,
    }

    return render(request, "store/index.html", context)


# =============================================================
# ======================Product Detail========================
# =============================================================
def product_detail(request, category_slug, product_slug):
    """Render the product detail page for a single product.

    Looks up the :class:`store.models.Product` scoped to its parent
    :class:`store.models.Category` so that slugs remain unique only within
    a category (industry-standard SEO convention). Also computes cart-aware
    flags used by the ``Add to cart`` button on the PDP:

    * ``in_cart``  - whether the current visitor already has this product
                     in their cart (used to toggle the CTA).
    * ``cart_qty`` - quantity currently in the cart (used for the qty stepper).

    Context:
        product  (Product):    The resolved product instance.
        category (Category):   The parent category (used for breadcrumbs).
        in_cart  (bool):       ``True`` if the product is already in cart.
        cart_qty (int):        Quantity currently in the visitor's cart.
    """
    # Sentinel value overwritten below once we know whether the product is in
    # the visitor's cart. Kept as a local for readability of the final context.
    in_cart = False
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product, slug=product_slug, category=category, is_available=True
    )
    # Check if in cart
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=product
    ).exists()
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
        "cart_qty": cart_qty,  # THIS IS THE KEY
        "in_cart": in_cart,
    }
    return render(request, "store/detail.html", context)





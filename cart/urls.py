"""URL configuration for the ``cart`` application.

Cart URLs are intentionally short and explicit. They live under the ``cart``
namespace so templates can use ``{% url 'cart:<name>' %}`` regardless of the
prefix used at the project level.

Routes:
    - ``/cart/add/<product_id>/``    -> ``add_cart``           (increment qty)
    - ``/cart/decrease/<id>/``       -> ``decrease_cart``      (decrement qty)
    - ``/cart/remove/<id>/``         -> ``remove_cart_item``   (delete row)
    - ``/cart/``                     -> ``cart``               (cart page)
"""

from django.urls import path

from . import views


# Application namespace used by ``reverse()`` and the ``{% url %}`` tag.
app_name = "cart"

#: URL patterns for the cart. The order is purely cosmetic — Django resolves
#: by path converter (``<int:product_id>``), not by position.
urlpatterns = [
    # ------------------- Cart view --------------------
    # The cart page itself, showing line items, totals and taxes.
    path("cart/", views.cart, name="cart"),
    # ------------------- Adding cart view --------------------
    # Increment quantity for a given product. If the visitor has no cart yet,
    # one is created on-demand and persisted against the session.
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    # ------------------- Removing cart view --------------------
    # Decrement quantity for a given product. When the quantity reaches zero
    # the line item is removed entirely.
    path(
        "decrease_cart/<int:product_id>/",
        views.decrease_cart,
        name="decrease_cart",
    ),
    # ------------------- Removing cart view --------------------
    # Hard-delete a single line item, regardless of its current quantity.
    path(
        "remove_cart/<int:product_id>/",
        views.remove_cart_item,
        name="remove_cart",
    ),
]

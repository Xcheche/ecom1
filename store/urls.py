"""URL configuration for the ``store`` application.

This module wires the public-facing storefront URLs to their corresponding
view functions. It is mounted under the ``store`` namespace so that templates
can reference routes with the ``{% url 'store:<name>' %}`` template tag.

Routes:
    - ``/``                                  -> ``store``              (homepage / catalog)
    - ``/<category_slug>/``                  -> ``category_view``      (category listing)
    - ``/product/<category_slug>/<slug>/``   -> ``product_detail``     (PDP)
"""

from django.urls import path

from . import views


# Application namespace used by ``reverse()`` and the ``{% url %}`` tag.
app_name = "store"

#: URL patterns for the storefront. Kept intentionally small — every route is
#: read once at import time and dispatched by Django's resolver.
urlpatterns = [
    # Homepage / catalog landing page. Renders the storefront with all
    # available products.
    path("", views.store, name="store"),
    # Category-filtered catalog view. ``category_slug`` is optional in the
    # view layer, but the URL pattern requires it for clean, shareable links.
    path(
        "<slug:category_slug>/",
        views.category_view,
        name="category_view",
    ),
    # Product detail page (PDP). The full slug chain keeps links SEO-friendly
    # and disambiguates products that may share a slug across categories.
    path(
        "product/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
]

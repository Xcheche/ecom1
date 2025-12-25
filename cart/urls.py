from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    # -------------------Cart view --------------------
    path("cart/", views.cart, name="cart"),
    # -------------------Adding cart view --------------------
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),

    #-------------------Removing cart view --------------------
    path("decrease_cart/<int:product_id>/", views.decrease_cart, name="decrease_cart"),
    #-------------------Removing cart view --------------------
    path("remove_cart/<int:product_id>/", views.remove_cart_item, name="remove_cart"),
]

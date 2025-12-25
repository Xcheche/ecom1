from django.contrib import admin
from .models import Cart, CartItem

#Tabular inline for CartItem model
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ("cart_id", "date_added")
    search_fields = ("cart_id",)    


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)


# Register your models here.

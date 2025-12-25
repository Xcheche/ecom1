from django.contrib import admin
from .models import Product, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "slug", "description", "category_image")
    prepopulated_fields = {"slug": ("category_name",)}
    search_fields = ("category_name", "description")
    list_filter = ("category_name",)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "slug",
        "current_price",
        "is_available",
        "stock",
        "average_rating",
        "review_count",
        "sale_start",
        "sale_end",
    )
    prepopulated_fields = {"slug": ("product_name",)}
    search_fields = ("product_name", "description", "short_description")
    list_filter = ("is_available", "stock", "current_price")
    list_editable = ("is_available", "stock", "current_price", "sale_start", "sale_end")
    prepopulated_fields = {"slug": ("product_name",)}


admin.site.register(Product, ProductAdmin)

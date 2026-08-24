from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(
        upload_to="category_images/%Y/%m/%d/", blank=True, null=True
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    # Get url
    def get_absolute_url(self):
        return reverse("store:category_view", args=[self.slug])


# Product model
class Product(models.Model):
    """Model representing a product in the store."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    product_name = models.CharField(
        max_length=200, unique=True, help_text="Enter product name..."
    )
    slug = models.SlugField(max_length=200, unique=True)

    short_description = models.CharField(
        max_length=100, blank=True, help_text="brief description of the product.."
    )
    description = models.TextField(
        max_length=700, blank=True, help_text="describe the product.."
    )
    additional_info = models.TextField(
        max_length=1000, blank=True, help_text="additional info of the product.."
    )
    product_image1 = models.ImageField(upload_to="product_images/%Y/%m/%d/")
    product_image2 = models.ImageField(upload_to="product_images/%Y/%m/%d/")
    product_image3 = models.ImageField(upload_to="product_images/%Y/%m/%d/")
    product_image4 = models.ImageField(upload_to="product_images/%Y/%m/%d/")

    # ===Price===
    price = models.IntegerField()

    # ===Check if the product is in stock and available for purchase===
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    # Check if the product is digital or physical
    # is_digital = models.BooleanField(default=False) for things that wont be shipped

    # ===Track product ratings and reviews====
    average_rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)

    # ===Timestamps===
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    ##Better to use django taggit for product tags

    # String representation
    def __str__(self):
        return f"{self.product_name} ({self.price})"

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    # get url
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug, self.slug])

    @property
    def new_product(self):
        """Return True if the product was created within the last 30 days."""
        from django.utils import timezone
        from datetime import timedelta

        return self.created_date >= timezone.now().date() - timedelta(days=30)

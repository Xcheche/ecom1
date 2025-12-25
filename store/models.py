from django.utils import timezone
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

    # ===Determine if the product is on sale===
    previous_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)

    # ===Check if the product is in stock and available for purchase===
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    # Check if the product is digital or physical
    # is_digital = models.BooleanField(default=False) for things that wont be shipped

    # ===Track product ratings and reviews====
    average_rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)

    # ===SEO fields===
    meta_title = models.CharField(max_length=100, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)

    # ===Timestamps===
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    ##Better to use django taggit for product tags

    # ===New arrivals tracking===

    new_since = models.DateTimeField(null=True, blank=True)

    # New arrivals logic
    @property
    def new(self):
        if not self.new_since:
            return False
        return timezone.now() - self.new_since < timezone.timedelta(
            days=30
        )  # new = created within last 30 days

    # Discount logic

    @property
    def is_on_sale(self):
        """Check if the product is currently on sale based on the sale period."""
        now = timezone.now()
        return (
            self.sale_start
            and self.sale_end
            and self.sale_start <= now <= self.sale_end
        )

    @property
    # def display_price(self):
    #     """Return the price to display based on whether the product is on sale."""
    #     if self.is_on_sale:
    #         return self.current_price
    #     return self.previous_price or self.current_price
  
    def display_price(self):
        return self.current_price


    # String representation
    def __str__(self):
        return f"{self.product_name} ({self.current_price})"

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    # get url
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug, self.slug])

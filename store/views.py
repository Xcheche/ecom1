from django.shortcuts import get_object_or_404, render

from store.models import Category,Product

# Create your views here.


def store(request):
    try:
        products = Product.objects.all().filter(is_available=True)
    except Exception:
        # Handle the case where products are not found
        return render(request, '404.html', status=404)
    context = {
        'products': products,
    }
    return render(request, 'store/index.html', context)

#Category view
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
        'category': category,
        'products': products,
        'product_count': product_count,
        # 'links' will come from your context processor automatically
    }

    return render(request, 'store/index.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, slug=product_slug, category=category, is_available=True)
    except Exception as e:
        # Handle the case where the category or product is not found
        raise e
    context = {
        'product': product,
        'category': category,

    }
    return render(request, 'store/detail.html', context)
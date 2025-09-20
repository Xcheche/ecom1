from .models import Product

from django.db.models import Count
from .models import Category, Product




# def menu_links():
#     """Context processor to add menu links (categories) to all templates.
#     It retrieves all Category objects and makes them available in the template context  as dict 
#     This link variable can then be used anywhere in the templates to display category links.
#     Dont forget in settings.py to add the context processor to TEMPLATES option
#     'OPTIONS': {
#         'context_processors': [
#     """
#     links = Category.objects.all()

#     links = Category.objects.annotate(product_count=Count('product'))
#     return dict(links=links)


def menu_links(request):
    links = Category.objects.annotate(product_count=Count('products'))
    return dict(links=links)

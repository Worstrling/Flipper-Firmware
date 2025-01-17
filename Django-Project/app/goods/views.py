from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404
from rest_framework import viewsets
from goods.models import Products, Categories
from goods.serializers import CategoriesSerializer, ProductsSerializer
from goods.utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, per_page=6)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Главная - Каталог',
        'goods': current_page,
        'slug_url': category_slug
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }
    return render(request, 'goods/product.html', context=context)


# -----------------api-----------------

class CategoryApiView(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class ProductApiView(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
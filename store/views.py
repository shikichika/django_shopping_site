
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
# pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from carts.views import _cart_id

from .models import Product
from category.models import Category
from carts.models import Cart, CartItem

# storeページとカテゴリごとんページ


def store(request, category_slug=None):
    categories = None
    paged_products = None

    # slugが指定されたら
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        # ページネーション
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # ページネーション
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        # pagenationを反映
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

# 商品の詳細


def product_detail(request, category_slug, product_slug):
    try:
        # __　はシンタックス category内のslugという意味
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)

        # productがカートにあるかどうか
        cart = Cart.objects.get(cart_id=_cart_id(request))
        in_cart = CartItem.objects.filter(
            cart=cart, product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

# 検索機能


def search(request):
    paged_products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by("create_date")
            product_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
        else:
            products = Product.objects.all().filter(is_available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            products_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

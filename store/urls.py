from django.urls import path

from . import views

urlpatterns = [
    path("", views.store, name='store'),
    #カテゴリーごとのページ
    path("category/<slug:category_slug>", views.store, name='products_by_category'),
    #商品の詳細
    path("category/<slug:category_slug>/<slug:product_slug>", views.product_detail, name='product_detail'),
    #商品検索
    path('search/', views.search, name='search'),
    
] 

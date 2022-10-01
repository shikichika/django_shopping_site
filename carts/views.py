from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product, Variation
from .models import Cart, CartItem

#sessionにcard_idを入れる
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

#cartに入れる
def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)#商品を特定
    product_variation = []
    if request.method =="POST":
        #商品の設定の動的な選択肢のために
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                #iexactは大文字小文字を意識しない
                variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact = value)
                product_variation.append(variation)
            except:
                pass     
            

    
    #既にカートに商品が入っていてカートが存在する時
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    #初めて商品を追加するのでカートが存在しない時
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    #カートに既に商品が含まれているとき
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list =[]
        id =[]
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        #size, colorが同じアイテムがカートにある時
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity +=1
            item.save()
        else:
            #size, colorが違うアイテムとしてはカートにあるアイテムを追加するとき
            cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart)

            if len(product_variation) > 0:
                cart_item.variations.clear()        
                cart_item.variations.add(*product_variation)
            cart_item.save()
    #カートに初めて商品が追加される時
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        if len(product_variation) > 0:
            #cartにある商品の詳細設定を一旦削除
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    
    return redirect('cart')


#カートからアイテムの個数を削除する
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart')

#カートのアイテム自体を消去する
def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    #cartが既にある時
    try:
        #cartがforeign_keyだから
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
            total +=(cart_item.product.price*cart_item.quantity)
        tax = (10*total)/100
        grand_total = total + tax          
    #cartがまだない時
    except:
        pass

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'store/cart.html', context)


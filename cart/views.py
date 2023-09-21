from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from cart.models import Wishlist, Cart, CartItem
from django.contrib.auth.decorators import login_required 
from products.models import Category
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def AddWishlistItem(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user = request.user
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.filter(user=user, product=product).exists()
    if not wishlist:
        Wishlist.objects.create(user=user, product=product)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def ShowWishlist(request):
    if not request.user.is_authenticated:
        return redirect('signin') 
    
    
    categories = Category.objects.all()
    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = 0
    if not wishlist:
        return render(request, 'wishlist/empty-wishlist.html', {'wishlist_count': wishlist_count})
    
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    context = {
        'wishlist': wishlist,
        'wishlist_count': wishlist_count,
        'categories': categories,
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def DeleteWishlistItem(request, id):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    wishlist = get_object_or_404(Wishlist, id=id)
    if wishlist:
        wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def clear_wishlist(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user = request.user
    wishlist =Wishlist.objects.filter(user=user)
    for item in wishlist:
        item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def add_to_cart(request, id):
    user = request.user
    cart = Cart.objects.filter(user=user).exists()
    product = Product.objects.get(id=id)
    if not cart:
        cart = Cart.objects.create(user=user)
    else:
        cart = Cart.objects.get(user=user)
    cart_item_exists = CartItem.objects.filter(cart=cart, product=product).exists()
        
    if cart_item_exists:
        cart_Item = CartItem.objects.get(cart=cart, product=product)
        cart_Item.quantity += 1
        cart_Item.save()
    else:
        CartItem.objects.create(cart=cart, product=product)
    
    return redirect(request.META.get('HTTP_REFERER'))
@login_required
def show_cart(request):
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    if not cart:
        return render(request, 'cart/empty-cart.html')
    
    cart_item = CartItem.objects.filter(cart=cart[0])
    if not cart_item:
        if cart:
            cart.delete()
        return render(request, 'cart/empty-cart.html')
   
    
    return render(request, 'cart/show_cart.html')

@login_required
def delete_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    
    if cart_item:
        cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def clear_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.filter(cart=cart)
    
    for item in cart_item:
        item.delete()
    cart.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    
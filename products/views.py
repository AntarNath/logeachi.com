from django.shortcuts import render, redirect
from  products.models import Product, Category, Main_Category, Subcategory, Product_Reviews_and_Rating
from django.core.paginator import Paginator
from cart.models import Wishlist
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required


# Create your views here.    

def sub_category_products(request, pk):
 
    products = Product.objects.filter(product_category=pk)
    main_categories = Main_Category.objects.all()
    sub_category = None
    category = None
    main_category = None
    
    sub_category = Subcategory.objects.get(id=pk)
    category = sub_category.category
    main_category = category.main_category
    product_count = products.count()
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)


def category_products(request, pk):
    main_categories = Main_Category.objects.all()
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category__category=category)
    product_count = products.count()
    sub_category = None
    main_category = category.main_category
    
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)


def main_category_products(request, pk):
    main_categories = Main_Category.objects.all()
    main_category = Main_Category.objects.get(id=pk)
    products = Product.objects.filter(product_category__category__main_category=main_category)
    product_count = products.count()
    sub_category = None
    category = None
    
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    context = {
        'main_categories': main_categories,
        'products': products,
        'main_category': main_category,
        'sub_category': sub_category,
        'category': category,
        'product_count': product_count,
        'wishlist_count': wishlist_count
    }
    return render(request, 'products/category_products.html', context)


def single_product_page(request, pk):
    product = Product.objects.get(id=pk)
    wishlist_count = 0
    avarage_rating = product.average_rating()
    reviews = Product_Reviews_and_Rating.objects.filter(product=product)
    review_count = reviews.count()
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    context = {
        'product': product,
        'wishlist_count': wishlist_count,
        'reviews': reviews,
        'review_count': review_count,
        'avarage_rating': avarage_rating,
    }
    return render(request, 'products/single_product_page.html', context)



@login_required
def add_review_rating(request):
   
    if not request.user.is_authenticated:
       return redirect('signup')
   
    if request.method == "POST":
        # Get the review and rating data from the form
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')
        product_id = request.POST.get('product_id')
        # print("======================================================", product_id)
        product = Product.objects.get(id=product_id)

        # Create a new review and rating entry in the database
        product_review = Product_Reviews_and_Rating.objects.create(
            product=product,
            user=request.user,
            review=review_text,
            rating=rating
        )

        # Redirect to a success page or product detail page
        return redirect('single_product_page', pk=product.id)

    else:
        # Handle GET requests or other methods as needed
        return JsonResponse({"error": "Invalid request method"}, status=400)












# def add_review(request, pk):
#     get_method =  request.GET.copy()
#     review = get_method.get('review')
#     name = get_method.get('name')
#     email = get_method.get('email')
#     product = Product.objects.get(id=pk)
#     if review is not None and name is not None and email is not None and product is not None:
#         Product_Reviews.objects.create(product=product, user_name=name, user_email=email, review=review)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
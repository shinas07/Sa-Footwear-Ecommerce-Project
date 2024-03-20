from django.shortcuts import render, get_object_or_404 ,redirect
from .models import Product,Brand,Category,ProductSizeColor, Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Cart.models import Cart,CartItem


def product(request):
    products = Product.objects.fiter(is_available= True,category__is_listed=True)
    context = {
        'products': products,
    }
    return render(request,'home.html',context)



def category_collections(request,category_name):
    category_name = category_name.title()
    category = get_object_or_404(Category,category_name=category_name)
    products = Product.objects.filter(category__is_listed=True,is_available=True,category=category)
    brands = Brand.objects.filter(category=category,is_active=True)

    # Set the active category for the template
    active_category = category_name.lower()

    context = {
        'brands': brands,
        'products': products,
        'gender': category_name,
        'category': category,
        'active_category': active_category,

    }
    return render(request,'collection.html',context)



def product_detail(request,product_id):
    request.session['product_id'] = product_id
    product = get_object_or_404(Product, pk=product_id, is_available=True, category__is_listed=True)
    product_size_colors = ProductSizeColor.objects.filter(product_id=product_id,is_unlisted=False)
    selected_product_stock = ProductSizeColor.objects.filter(product=product).first()

    
    context =  {
    'product': product,
    'product_size_colors': product_size_colors,
    'selected_product_size' :selected_product_stock,
    }

    return render(request, 'product_details.html',context)
    

    
    

@login_required(login_url='Accounts:login')
def stock_of_size(request,size_id):
    session_id = request.session.get('product_id')
    product = get_object_or_404(Product, pk=session_id, is_available=True, category__is_listed=True)
    product_size_colors = ProductSizeColor.objects.filter(product_id=session_id,is_unlisted=False)
    selected_product_size = get_object_or_404(ProductSizeColor, pk=size_id, product=product)
    
    context =  {
    'product': product,
    'product_size_colors': product_size_colors,
    'selected_product_size' :selected_product_size,
    }

    return render(request, 'product_details.html',context)

   


def brand_wise_products(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    products = Product.objects.filter(product_brand=brand)
    context = {
        'brand': brand,
        'products': products,
    }
    return render(request, 'collection.html', context)
  

# WISHLIST

@login_required(login_url='Accounts:login')
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.get(customer=request.user)
    except Wishlist.DoesNotExist:
        wishlist = None
    
    
    if wishlist:
        products = wishlist.products.all()
        product_stocks = ProductSizeColor.objects.filter(product__in=products)

    else:
        products = []
        product_stocks = []

    return render(request, 'add_to_wishlist.html', {'products': products, 'product_stocks': product_stocks})





# @login_required(login_url='Accounts:login')
# def wishlist_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     if created:
#         cart.save()

#     product_size_colors = ProductSizeColor.objects.filter(product=product)

#     # Check if any ProductSizeColor instance has stock greater than zero
#     has_stock = any(product_size_color.Stock > 0 for product_size_color in product_size_colors)

#     if not has_stock:
#         messages.error(request, 'Product is Out of Stock')
#         return redirect('product:wishlist_view')

#     if CartItem.objects.filter(cart=cart, product=product).exists():
#         messages.error(request, f"{product.product_name} is already in your cart.")
#         return redirect('product:wishlist_view')

#     # Assuming you want to add the first ProductSizeColor instance with stock to the cart
#     # Adjust this logic as needed based on your requirements
#     product_size_color = product_size_colors.filter(Stock__gt=0).first()
#     if product_size_color:
#         CartItem.objects.create(cart=cart, product=product, quantity=1)
#         messages.success(request, f"{product.product_name} added to cart successfully.")
#         return redirect('product:wishlist_view')
#     else:
#         messages.error(request, 'Product is Out of Stock')
#         return redirect('product:wishlist_view')


@login_required(login_url='Accounts:login')
def add_to_wishlist(request, product_id):
    category_name = None  
    
    if request.method == 'POST':
        try:
            wishlist = Wishlist.objects.get(customer=request.user)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(customer=request.user)
            
        product = get_object_or_404(Product, pk=product_id)
        

        if wishlist.products.filter(pk=product_id).exists():
            messages.info(request, 'This product is already in your wishlist.')
        else:
            # Add the product to the wishlist
            wishlist.products.add(product)
            messages.success(request, 'Product added to wishlist successfully.')
            
    
        return redirect('product:wishlist_view')  
    
    return redirect('product:wishlist_view')



def remove_from_wishlist(request, product_id):
    customer = request.user 
    wishlist = get_object_or_404(Wishlist, customer=customer)
    
    product = get_object_or_404(Product, pk=product_id)
    
    wishlist.products.remove(product)
    
    messages.success(request, 'Product removed from wishlist successfully.')
    return redirect('product:wishlist_view')
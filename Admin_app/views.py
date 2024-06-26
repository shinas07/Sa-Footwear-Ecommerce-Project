from calendar import month_name
from django import forms
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from Accounts.models import Customer
from Cart.models import Coupon
from Category.models import Category
from Products.models import Product,Brand,ProductSizeColor
from .forms import BannerForm, ProductForm,CouponForm, TimeFrameForm,BrandForm,ProductSizeColorForm,ProductOfferForm
from Home.models import Banner, Wallet
from django.views import View
from Orders.models import Order, OrderProduct
from django.db.models import Sum,Count
from datetime import datetime, timedelta
from .models import ProductOffer, Sale
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.db.models import F
from django.urls import reverse
import io
from Admin_app import forms
from django.utils import timezone
from openpyxl.worksheet.table import Table
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth 
from collections import Counter




def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard') 
        else:
            error_message = 'Incorrect username or password.'
            # return redirect('admin_login') 
            return render(request, 'admin_login.html', {'error_message': error_message})  
    else:
        return render(request, 'admin_login.html')  
    


@login_required(login_url='admin_login')
def admin_dashboard(request):
    if request.user.is_superuser:
        online_sales_count = Order.objects.filter(orderproduct__status='Delivered', payment_method='Paid by Razorypay').count()
        overall_sales_count = OrderProduct.objects.filter(status='Delivered').count()
        cod_sale_count = Order.objects.filter(orderproduct__status='Delivered', payment_method='COD').count

        overall_cod_amount = Order.objects.filter(orderproduct__status='Delivered',payment_method='COD').aggregate(Sum('total_amount'))['total_amount__sum']
        overall_online_amount = Order.objects.filter(orderproduct__status='Delivered',payment_method='Paid by Razorypay').aggregate(Sum('total_amount'))['total_amount__sum']
        overall_order_amount = Order.objects.filter(orderproduct__status='Delivered').aggregate(Sum('total_amount'))['total_amount__sum']
        overall_discount = ProductOffer.objects.aggregate(total_discount=Sum('discount_percentage'))['total_discount']

        #best_selling_products
        best_selling_products = OrderProduct.objects.values('product__id', 'product__product_name', 'product__category__category_name', 'product__product_brand__brand_name').annotate(total_orders=Count('product')).order_by('-total_orders')[:10]

        #best_selling_Brand
        brand_sales = Product.objects.values('product_brand__brand_name').annotate(total_orders=Count('id')).order_by('-total_orders')[:5]



        context = {
        'online_sales_count':online_sales_count,
        'cod_sale_count': cod_sale_count,
        'overall_sales_count':overall_sales_count,
        'overall_cod_amount' :overall_cod_amount,
        'overall_online_amount':overall_online_amount,
        'overall_order_amount': overall_order_amount,
        'overall_discount': overall_discount,
        'best_selling_products':best_selling_products,
        'brand_sales' :brand_sales,
    }
        return render(request, 'admin_index.html',context)
    else:
        return redirect('/')


class ChartData(View):
    def get(self, request):
        year = request.GET.get('year')  # Get the year from the query parameters
        # Retrieve the count of orders for each month
        if year:
            order_data = Order.objects.filter(created_at__year=year).annotate(month=ExtractMonth('created_at')).values('month').annotate(total_orders=Count('id'))
        else:
            order_data = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(total_orders=Count('id'))

        month_data = {month: 0 for month in range(1, 13)}

        # Populate the dictionary with data from the queryset
        for entry in order_data:
            month_data[entry['month']] = entry['total_orders']

        # Extracting labels (months) and chart data (total orders)
        labels = [month_name[i] for i in range(1, 13)]
        chart_data = [month_data[i] for i in range(1, 13)]


        data = {
            "labels": labels,
            "chartLabel": "Order Count per Month",
            "chartdata": chart_data,
        }
        return JsonResponse(data)

@login_required(login_url='admin_login')
def admin_users(request):
    if request.user.is_superuser:
        users = Customer.objects.filter(is_staff=False).order_by('-id')
        return render(request,'admin_curd.html',{'users':users})
    else:
        return redirect('/')

@login_required(login_url='admin_login')
def block_user(request,user_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(Customer,pk=user_id)
            user.is_blocked = True
            user.save()
            messages.success(request, "User blocked successfully.")
            return redirect('admin_users')
    else:
        return redirect('/')

@login_required(login_url='admin_login')
def unblock_user(request,user_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(Customer,pk=user_id)
            user.is_blocked = False
            user.save()
            return redirect('admin_users')
    else:
        return redirect('/')
    
@login_required(login_url='admin_login')  
def admin_category(request):
    if request.user.is_superuser:
        categorys = Category.objects.all().order_by('-id')
        return render(request, 'admin_category.html', {'categorys': categorys, 'messages': messages.get_messages(request)})
    else:
        return redirect('/')
    
@never_cache
@login_required(login_url='admin_login')
def admin_product(request):
    if request.user.is_superuser:
        products = Product.objects.all().order_by('-created_at')
        product_size_colors = ProductSizeColor.objects.filter(is_unlisted=False)
        brands = Brand.objects.filter(is_active=True)
        context = {
            'products' : products,
            'brands' : brands,
            'product_size_colors' : product_size_colors,


            
        }
        return render(request,'admin_product.html',context)
    else:
        return redirect('/')
    
@never_cache
@login_required(login_url='admin_login')
def admin_product_filter(request):
    # Get the selected category and brand from the query parameters
    selected_category = request.GET.get('category_filter', '')
    selected_brand = request.GET.get('brand_filter', '')
    brands = Brand.objects.filter(is_active=True)
    product_size_colors = ProductSizeColor.objects.filter(is_unlisted=False)

    # Initialize an empty queryset for products
    products = Product.objects.all()

    if selected_category:
        products = products.filter(category__category_name=selected_category)

    if selected_brand:
        products = products.filter(product_brand__brand_name=selected_brand)

    # Render the template with the filtered products
    context = {
        'products': products,
        'brands' : brands,
        'product_size_colors':product_size_colors,
        }
    return render(request, 'admin_product.html', context)


@login_required(login_url='admin_login')
def admin_add_product(request):
    if request.user.is_superuser:
    # categories = Category.objects.all()
        if request.method == 'POST':
            product_form = ProductForm(request.POST,request.FILES)
            product_size_color_form = ProductSizeColorForm(request.POST)
            if product_form.is_valid():
                product = product_form.save()
                messages.success(request,'Product added successfully!')
                return redirect('admin_product')
            else:
                FIELD_NAME_MAPPING = {
                    'product_name': 'Product Name',
                    'description': 'Description',
                    'price': 'Price',
                    'category': 'Category',
                    'is_available': 'Availability',
                    'product_brand': 'Brand',
                    'left_view_image': 'Left View Image',
                    'right_view_image': 'Right View Image',
                    'full_view_image': 'Full View Image',
                }
                for field, errors in product_form.errors.items():
                    for error in errors:
                        field_name = FIELD_NAME_MAPPING.get(field,field)
                        messages.error(request, f"{field_name } : {error}")
                return render(request, 'admin_add_product.html', {'product_form': product_form})
        else:
            product_form = ProductForm()
            return render(request, 'admin_add_product.html', {'product_form': product_form})
    else:
        return redirect('/')



@login_required(login_url='admin_login')
def edit_product(request, pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=pk)
        product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        if request.method == 'POST':
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('admin_product')
            else:
                FIELD_NAME_MAPPING = {
                    'product_name': 'Product Name',
                    'description': 'Description',
                    'price': 'Price',
                    'category': 'Category',
                    'is_available': 'Availability',
                    'product_brand': 'Brand',
                    'left_view_image': 'Left View Image',
                    'right_view_image': 'Right View Image',
                    'full_view_image': 'Full View Image',
                }
                for field, errors in product_form.errors.items():
                    for error in errors:
                        field_name = FIELD_NAME_MAPPING.get(field,field)
                        messages.error(request, f"{field_name } : {error}")
                        return render(request, 'admin_edit_product.html', {'product_form': product_form})
                    
        return render(request, 'admin_edit_product.html', {'product_form': product_form,})
    else:
        return redirect('/')
    




from django.forms.models import modelformset_factory

@login_required(login_url='admin_login')
def edit_product_size_color(request, pk):
    if request.user.is_superuser:
        if pk:
            product = get_object_or_404(Product, id=pk)
            queryset = ProductSizeColor.objects.filter(product=product)

            # Create the formset using modelformset_factory
            ProductSizeColorFormSet = modelformset_factory(ProductSizeColor, form=ProductSizeColorForm, extra=0)

            if request.method == 'POST':
                formset = ProductSizeColorFormSet(request.POST, queryset=queryset)
                if formset.is_valid():
                    formset.save()
                    messages.success(request, 'Product size and color updated successfully!')
                    return redirect('admin_product')
                else:     
                    messages.error(request, 'Please correct the errors below.')
    
            else:
                formset = ProductSizeColorFormSet(queryset=queryset)
            return render(request, 'admin_edit_product_size_color.html', {'formset': formset})
        else:
            messages.error(request, 'Product ID is required.')
            return redirect('admin_product')
    else:
        return redirect('/')



@login_required
def unlist_product(request,pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product,pk=pk)
        product.is_available  = False
        product.save()
        return redirect('admin_product')
    else:
        return redirect('/')

@login_required
def list_product(request,pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product,pk=pk)
        product.is_available = True
        product.save()
        return redirect('admin_product')
    else:
        return redirect('/')

@login_required
def product_size_color(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductSizeColorForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product size and color added successfully!')
                return redirect('admin_product')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ProductSizeColorForm()
        return render(request, 'admin_product_size_color.html', {'form': form})
    else: 
        return redirect('/')





@login_required
def admin_add_brand(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        brands = Brand.objects.all()  
        if request.method == 'POST':
            form = BrandForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('brand_name')

                if Brand.objects.filter(brand_name=name).exists():
                    messages.error(request,'Brand already exsists.')
                else:
                    form.save()
                    messages.success(request, 'Brand added successfully.')
                    return redirect('admin_add_brand')  
        else:
            form = BrandForm()
        return render(request, 'admin_add_brand.html', {'form': form, 'categories': categories, 'brands': brands})
    else:
        return redirect('/')

@login_required
def block_brand(request,brand_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            brand = Brand.objects.get(id=brand_id)
            brand.is_active = False
            brand.save()
            return redirect('admin_add_brand')
    else:
        return redirect('/')
    
@login_required
def unblock_brand(request,brand_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            brand = Brand.objects.get(id=brand_id)
            brand.is_active = True
            brand.save()
            return redirect('admin_add_brand')
    else:
        return redirect('/')
        
@login_required
def edit_brand(request,brand_id):
    if request.user.is_superuser:
        brand = get_object_or_404(Brand, id=brand_id) 
        if request.method == 'POST':
            form = BrandForm(request.POST,request.FILES,instance=brand)
            if form.is_valid():
                form.save()
                return redirect('admin_add_brand')
            else:
                messages.error(request, 'Error updating brand. Please check it correctly.')
        else:
            form = BrandForm(instance=brand)
        return render(request,'admin_edit_brand.html',{'form':form,'brand':brand})
    else:
        return redirect('/')




@login_required(login_url='admin_login')
def admin_order_management(request):
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-id')

        filter_value = request.GET.get('filter')
        if filter_value:
            orders = orders.filter(payment_method=filter_value)
            return render(request, 'manage_order.html', {'orders': orders})
        
        return render(request, 'manage_order.html', {'orders': orders})
    else:
        return redirect('/')

@login_required(login_url='admin_login')
def order_products_details(request,order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        order_products = order.orderproduct_set.all()
        return render(request, 'manage_order_details.html', {'order': order, 'order_products': order_products})
    else:
        return redirect('/')



@login_required(login_url='admin_login')
def admin_product_status(request, order_id, order_product_id):
    if request.user.is_superuser:
        order_product = get_object_or_404(OrderProduct, id=order_product_id)
        # result = OrderProduct.objects.get(order = order_product_id)
        if request.method == 'POST':
            new_status = request.POST.get('new_status')
            if new_status:
                order_product.status = new_status
                if new_status == 'Returned' and order_product.order.payment_method == 'Paid by Razorypay' :
                    if order_product.product.offer_price:
                        user_wallet = Wallet.objects.get(user=order_product.order.user)
                        product_price = order_product.product.offer_price
                        user_wallet.balance += product_price
                        user_wallet.save()
                    else:
                        user_wallet = Wallet.objects.get(user=order_product.order.user)
                        product_price = order_product.product.price

                        user_wallet.balance += product_price
                        user_wallet.save()
                    
                elif new_status == 'Cancelled' and order_product.order.payment_method == 'Paid by Razorypay':
                     
                    if order_product.product.offer_price:
                        user_wallet = Wallet.objects.get(user=order_product.order.user)
                        product_price = order_product.product.offer_price
                        user_wallet.balance += product_price
                        user_wallet.save()
                    else:
                        user_wallet = Wallet.objects.get(user=order_product.order.user)
                        product_price = order_product.product.price

                        user_wallet.balance += product_price
                        user_wallet.save()

                elif new_status == 'Delivered':
                    order_product.delivery_date = timezone.now()

                    # Create a Sale record for the delivered product
                    Sale.objects.create(
                        product=order_product.product,
                        quantity=order_product.quantity,
                        price=order_product.product.price,
                    )

                else:
                    order_product.delivery_date = None

                order_product.save()
                messages.success(request, 'Product status updated successfully')
                return redirect(reverse('order_products_details', kwargs={'order_id': order_id}))

            else:
                messages.error(request, 'Invalid status provided')

        return redirect("admin_order_management") 
    else:
        return redirect('/')
    


# admin_coupon_adding
@never_cache
@login_required(login_url='admin_login')
def admin_add_coupon(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CouponForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Coupon added successfully!')
                return redirect('admin_add_coupon')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = CouponForm()
        coupons = Coupon.objects.all()
        return render(request, 'admin_add_coupon.html', {'form': form,'coupons':coupons})
    else:
        return redirect('/')


def admin_delete_coupon(request,coupon_id):
    if request.method == 'POST':
        coupon = get_object_or_404(Coupon,id=coupon_id)
        coupon.delete()
        messages.success(request,'Coupon deleted successfully!')
        return redirect('admin_add_coupon')

@login_required(login_url='admin_login')
def admin_add_banner(request,baner_id):
    if request.user.is_superuser():
        banners = Banner.objects.all()
        if request.method =='POST':
            brand = Brand.objects.create()
            brand.save()
        else:
            return render(request,'admin_add_banner.html',{'banners':banners})
    else:
        return redirect('/')
        
@login_required(login_url='admin_login')
def admin_add_banner(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = BannerForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,'Banner Added Succesful')
                return redirect('admin_add_banner')
        banners = Banner.objects.all()
        form = BannerForm()
        return render(request, 'admin_add_banner.html', {'banners': banners, 'form': form})
    else:
        return redirect('/')

@login_required(login_url='admin_login')
def delete_banner(request, banner_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            banner = Banner.objects.get(id=banner_id)
            banner.delete()
            messages.success(request,'Banner Deleted')
            return redirect('admin_add_banner')
    else:
        return redirect('/')


#product sales report



@login_required(login_url='admin_login')
def admin_sales_report(request):
    if request.method == 'POST':
        form = TimeFrameForm(request.POST)
        if form.is_valid():
            time_frame = form.cleaned_data['time_frame']

            sales = get_sales_data(form, time_frame)  # Assuming get_sales_data retrieves relevant sales data

       
            sales_data = []

            for sale in sales:
    # Retrieve product details
                product_name = sale.product.product_name
                quantity = sale.quantity
                price = sale.price
                date = sale.date.strftime('%Y-%m-%d')


                # Calculate discount deduction based on offer price (if available)
                discount_deduction = (sale.product.price - sale.product.offer_price) * sale.quantity if sale.product.offer_price else 0
 

                # Initialize coupon deduction to 0
                coupon_deduction = 0


                order_products = OrderProduct.objects.filter(product=sale.product)
         
                if order_products.exists():
                    # Get the first order product to check if a coupon was applied to its order
                    order_product = order_products.first()

 
                # Calculate total deduction
                total_deduction = discount_deduction + coupon_deduction

                # Calculate total amount for the order
                total_amount = quantity * price - total_deduction
     

                # Add sale data to the list
                sales_data.append({
                    'product': product_name,
                    'quantity': quantity,
                    'price': str(price),
                    'date': date,
                    'discount_deduction': str(discount_deduction),
                    # 'coupon_deduction': str(coupon_deduction),
                    # 'total_deduction': str(total_deduction),
                    'total_amount'  :  str(total_amount)
                })
                


            request.session['sales_data'] = sales_data
            return render(request, 'admin_sales_report.html', {'form': form, 'sales': sales,'sales_data':sales_data})
    else:
        form = TimeFrameForm()
        sales = Sale.objects.filter(date__date=timezone.now().date())
        return render(request, 'admin_sales_report.html', {'form': form, 'sales': sales})




def get_sales_data(form, time_frame):
    now = timezone.now().date()
    if time_frame == 'daily':
        return Sale.objects.filter(date__date=now)
    elif time_frame == 'weekly':
        start_date = now - timedelta(days=7)
        return Sale.objects.filter(date__date__range=(start_date, now))
    elif time_frame == 'yearly':
        start_date = now - timedelta(days=365)
        return Sale.objects.filter(date__date__range=(start_date, now))
    elif time_frame == 'custom':
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return Sale.objects.filter(date__date__range=(start_date, end_date))






@login_required(login_url='admin_login')
def download_report(request):
    if request.method == 'POST':
        report_format = request.POST.get('report_format')
        sales_data = request.session.get('sales_data', [])
        time_frame = request.session.get('time_frame', 'custom') # Retrieve the time frame from the session

        if report_format == 'pdf':
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

             # Add a main heading
            styles = getSampleStyleSheet()
            heading_style = styles['Heading1']
            heading_style.textColor = colors.black
            heading_style.fontSize = 18
            heading_style.alignment = 1 # Centered
            heading = Paragraph("Product Report", heading_style)
            elements.append(heading)

            # Prepare the data for the table
            data = [['Product', 'Quantity', 'Price', 'Discount','total_amount']] + [
            [sale['product'], sale['quantity'], sale['price'], sale['discount_deduction'], sale['total_amount']] for sale in sales_data
        ]

            # Create a table with the data
            table = Table(data)

            # Apply table styling
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ])
            table.setStyle(style)

            # Add the table to the document
            elements.append(table)

            # Build the PDF
            doc.build(elements)

            buffer.seek(0)

            # Construct the filename based on the time frame
            filename = f"{time_frame.capitalize()} Report.pdf"
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        elif report_format == 'excel':
            wb = Workbook()
            ws = wb.active
            ws.append(['Product Name', 'Quantity', 'Price','Discount','total_amount'])
            for sale in sales_data:
                ws.append([sale['product'], sale['quantity'], sale['price'], sale['discount_deduction'],sale['total_amount'] ])
            excel_file = io.BytesIO()
            wb.save(excel_file)
            wb.close()
            excel_file.seek(0)

            filename = f"{time_frame.capitalize()} Report.xlsx"
            response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    
   
        





@login_required(login_url='admin_login')
def discount_product_list(reqeust):
    products = Product.objects.filter(is_available=True,category__is_listed=True)
    return render(reqeust,'discount_product_list.html',{'products':products,})


@login_required(login_url='admin_login')
def set_product_discount(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.product = product

            offer.save()

            offer_price = product.price - (product.price * (offer.discount_percentage / 100))
            product.offer_price = offer_price
            product.save()
            messages.success(request, 'Discount set successfully.')
            return redirect('discount_product_list')
    else:
        form = ProductOfferForm()
    return render(request, 'set_product_discount.html', {'form': form, 'product': product})




@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')



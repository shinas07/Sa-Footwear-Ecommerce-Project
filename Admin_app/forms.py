from django import forms
from Products.models import Product,ProductSizeColor
# from django.core.files.uploadedfile import InMemoryUploadedFile
from django import forms
# from PIL import Image
# from io import BytesIO
from Products.models import Brand
from Home.models import Banner
from Cart.models import Coupon
from .models import ProductOffer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'category', 'is_available', 'product_brand', 'left_view_image', 'right_view_image', 'full_view_image']


    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        if not product_name.strip():  # Check if product name contains only whitespace
            raise forms.ValidationError(("Product name cannot be empty or contain only whitespace."))
        return product_name
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if not description.strip():
            raise forms.ValidationError(("Product name cannot be empty or contain only whitespace."))
        return description
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_left_image(self):
        image = self.cleaned_data.get('left_view_image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Please upload a valid image file (.png, .jpg, .jpeg) for left view image.")
            return image
        
    def clean_right_view_image(self):
        image = self.cleaned_data.get('right_view_image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError(("Please upload a valid image file (.png, .jpg, .jpeg) for right view image."))
        return image
    
    def clean_full_view_image(self):
        image = self.cleaned_data.get('full_view_image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError(("Please upload a valid image file (.png, .jpg, .jpeg) for full view image."))
        return image

class ProductSizeColorForm(forms.ModelForm):
    class Meta:
        model = ProductSizeColor
        fields = ['id','product','size','Stock','color','is_unlisted']

    # class Meta:
    #     model = ProductSizeColor
    #     fields = ['product', 'size', 'Stock', 'color', 'is_unlisted']

   
    def clean_Stock(self):
        stock = self.cleaned_data.get('Stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_image', 'category', 'is_active']

    def clean_brand_image(self):
        image = self.cleaned_data.get('brand_image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Please upload a valid image file (.png, .jpg, .jpeg)")
            return image


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['banner_name', 'banner_image']


    def clean_brand_image(self):
        image = self.cleaned_data.get('brand_iamge')
        if image:
            if not image.name.endswith(('.png','.jpg','.jpeg')):
                raise forms.VaildationError(("Please upload a valid image file (.png, .jpg, .jpeg) "))
            return image




class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'valid_from', 'valid_to', 'active']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        discount = cleaned_data.get('discount')

        if discount is not None:
            if discount < 0:
                raise ValidationError("Discount must be between 0 and 100.")

        return cleaned_data





class TimeFrameForm(forms.Form):
    TIME_FRAME_CHOICES = [
        ('daily', 'Today'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]

    time_frame = forms.ChoiceField(choices=TIME_FRAME_CHOICES, label='Time Frame')
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


#Form for product offer

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['discount_percentage', 'end_date']
        labels = {
            'discount_percentage': 'Discount (%)',
        }
    
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if discount_percentage < 0 or discount_percentage > 100:
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
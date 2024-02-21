from django import forms
from Products.models import Product
# from django.core.files.uploadedfile import InMemoryUploadedFile
from django import forms
# from PIL import Image
# from io import BytesIO
from Products.models import Brand
from Category.models import Category
from Home.models import Banner


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'size', 'price', 'stock', 'category', 'is_available', 'left_view_image', 'right_view_image', 'full_view_image','product_brand']

    # left_view_image = forms.ImageField(label='Image left view')
    # right_view_image = forms.ImageField(label='Image right view')
    # full_view_image = forms.ImageField(label='Image full view')
    # product_brand = forms.ModelChoiceField(queryset=Brand.objects.all())
        

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

class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_image','category']


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['banner_name', 'banner_image']




    # def save(self,*args, **kwargs):
    #     super().save(*args, *kwargs)
    #     img = Image.open(self.image.path)
    #     if img.hegiht > 40 or img.wight


    # def clean_left_view_image(self):
    #     return self.clean_image('left_view_image')

    # def clean_right_view_image(self):
    #     return self.clean_image('right_view_image')

    # def clean_full_view_image(self):
    #     return self.clean_image('full_view_image')

    # def clean_image(self, field_name):
    #     image = self.cleaned_data[field_name]
    #     if image:
    #         resized_image = self.process_image(image)
    #         return resized_image
    #     return image

    # def process_image(self, image):
    #     img = Image.open(image)
    #     # img.thumbnail((300, 300))
    #     img_resized = img.resize((500, 300))
    #     # if img.mode != 'RGB':
    #     #     img = img.convert('RGB')
    #     if img_resized.mode != 'RGB':
    #         img_resized = img_resized.convert('RGB')

    # # Create a BytesIO object to store the processed image data
    #     output = BytesIO()

    # # Save the image to BytesIO
    #     img.save(output, format='JPEG', quality=100)

    # # Move the file pointer to the beginning of the BytesIO object
    #     output.seek(0)

    # # Create an InMemoryUploadedFile object from BytesIO
    #     resized_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', len(output.getvalue()), None)
    #     return resized_image

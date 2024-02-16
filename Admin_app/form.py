from django import forms
from Products.models import Product
from django.core.files.uploadedfile import InMemoryUploadedFile
from django import forms
from PIL import Image
from io import BytesIO


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'size', 'price', 'stock', 'category', 'is_available', 'left_view_image', 'right_view_image', 'full_view_image']

    left_view_image = forms.ImageField(label='Image left view')
    right_view_image = forms.ImageField(label='Image right view')
    full_view_image = forms.ImageField(label='Image full view')


    def clean_left_view_image(self):
        return self.clean_image('left_view_image')

    def clean_right_view_image(self):
        return self.clean_image('right_view_image')

    def clean_full_view_image(self):
        return self.clean_image('full_view_image')

    def clean_image(self, field_name):
        image = self.cleaned_data[field_name]
        if image:
            resized_image = self.process_image(image)
            return resized_image
        return image

    def process_image(self, image):
        img = Image.open(image)
        # img.thumbnail((300, 300))
        img_resized = img.resize((500, 300))
        # if img.mode != 'RGB':
        #     img = img.convert('RGB')
        if img_resized.mode != 'RGB':
            img_resized = img_resized.convert('RGB')

    # Create a BytesIO object to store the processed image data
        output = BytesIO()

    # Save the image to BytesIO
        img.save(output, format='JPEG', quality=100)

    # Move the file pointer to the beginning of the BytesIO object
        output.seek(0)

    # Create an InMemoryUploadedFile object from BytesIO
        resized_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', len(output.getvalue()), None)
        return resized_image

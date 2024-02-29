from django import forms
from Products.models import ProductSizeColor
from django.db.models import Max

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,label='Quantity')

    def __init__(self,*args,**kwargs):
        product = kwargs.pop('product')
        super(AddToCartForm,self).__init__(*args,**kwargs)
        product_size_colors = ProductSizeColor.objects.filter(product=product)
        
        # Calculate the maximum stock available across all ProductSizeColor objects
        max_stock = product_size_colors.aggregate(Max('Stock'))['Stock__max']
        
        # Set the maximum value for the quantity field
        if max_stock is not None:
            self.fields['quantity'].widget.attrs['max'] = max_stock
        else:
            # Handle the case when there are no ProductSizeColor objects or no stock available
            self.fields['quantity'].widget.attrs['max'] = 0

from django import forms
from .models import Address

class CheckoutForm(forms.Form):
    address = forms.ModelChoiceField(queryset=None, label='Select Address')
    payment_method = forms.ChoiceField(choices=[('COD', 'Cash on Delivery')], label='Payment Method')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve 'user' from kwargs and remove it
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)

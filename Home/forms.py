from django import forms
from .models import Address
from django.core.validators import MinLengthValidator


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','address', 'House_no', 'city', 'state', 'country', 'pincode']

    def clean_House_no(self):
        house_no = self.cleaned_data.get('House_no')
        if not house_no.isdigit():
            raise forms.ValidationError("House number should be a valid number.")
        return house_no

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit pincode.")
        return pincode




class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput,validators=[MinLengthValidator(8)])
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'pincode']
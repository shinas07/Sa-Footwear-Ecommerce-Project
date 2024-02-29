from django import forms
from Home.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'House_no', 'city', 'state', 'country', 'pincode']




class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'pincode']
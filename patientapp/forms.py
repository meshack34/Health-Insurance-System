from .models import *
from django.forms import DateInput
from django.forms.fields import DateField
from django.forms.widgets import PasswordInput
from django import forms
from django.forms import DateInput, DateField, PasswordInput
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(attrs={
        
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', ]
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
    



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_image', 'city', 'address', 'country', 'date_of_birth', 'blood_group', 'gender']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs['class'] = 'upload'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'


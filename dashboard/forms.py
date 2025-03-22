from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["phone", "cellphone", "email", "social_url"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "exterior_num", "interior_num",
                  "colony", "city", "state", "postal_code"]


class LegalDataForm(forms.ModelForm):
    class Meta:
        model = LegalData
        fields = ["rfc", "company_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "surnames", "gender", "type"]


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ["name"]


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ["key", "name"]


class RegisterSessionForm(forms.ModelForm):
    class Meta:
        model = RegisterSession
        fields = ["total_sold", "initial_amount"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "existence", "existence_min",
                  "sale_price", "brand", "department", "size"]
        widgets = {
            "brand": forms.Select(),
            "department": forms.Select(),
            "size": forms.Select(),
        }

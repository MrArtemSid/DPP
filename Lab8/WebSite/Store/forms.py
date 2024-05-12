from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Sells, Storage, Item, Seller, SellerPlan, StoragePlan


class SellsForm(forms.ModelForm):
    class Meta:
        model = Sells
        fields = ["storage", "item", "cnt", "seller", "sell_data"]
        widgets = {
            'sell_data': forms.DateInput(attrs={'type': 'date'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = list([field.name for field in model._meta.fields])[1:]


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = list([field.name for field in model._meta.fields])[1:]

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = list([field.name for field in model._meta.fields])[1:]

class SellerPlanForm(forms.ModelForm):
    class Meta:
        model = SellerPlan
        fields = list([field.name for field in model._meta.fields])[1:]
        widgets = {
            'plan_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StoragePlanForm(forms.ModelForm):
    class Meta:
        model = StoragePlan
        fields = list([field.name for field in model._meta.fields])[1:]
        widgets = {
            'plan_date': forms.DateInput(attrs={'type': 'date'}),
        }



class UserSignForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

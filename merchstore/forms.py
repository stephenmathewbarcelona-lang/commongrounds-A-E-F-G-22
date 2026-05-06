from django import forms
from .models import Product, Transaction

class ProductAssembleForm(forms.ModelForm): # For Create and Update
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'stock', 'status', 'productType']
        widgets = {
            'productType': forms.Select,
            'status': forms.Select,
        }
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
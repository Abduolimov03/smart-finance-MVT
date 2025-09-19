from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'amount', 'payment_method']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nomi yoki manbai'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Summasi'}),
            'payment_method': forms.Select()
        }

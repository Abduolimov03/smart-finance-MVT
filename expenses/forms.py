from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'payment_method']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nomi yoki manbai'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Summasi'}),
            'payment_method': forms.Select(),
        }
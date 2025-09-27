from django import forms
from django.utils.translation import gettext_lazy as _
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'payment_method']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Nomi yoki manbai')}),
            'amount': forms.NumberInput(attrs={'placeholder': _('Summasi')}),
            'payment_method': forms.Select(),
        }
        labels = {
            'title': _('Nomi yoki manbai'),
            'amount': _('Summasi'),
            'payment_method': _('To‘lov turi'),
        }

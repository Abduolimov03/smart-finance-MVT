from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'amount', 'payment_method', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Nomi yoki manbai')}),
            'amount': forms.NumberInput(attrs={'placeholder': _('Summasi')}),
            'payment_method': forms.Select(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'title': _('Nomi yoki manbai'),
            'amount': _('Summasi'),
            'payment_method': _('To‘lov usuli'),
            'created_at': _('Sana'),
        }


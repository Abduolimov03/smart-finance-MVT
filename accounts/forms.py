from django import forms
from .models import CustomUser, VIA_EMAIL, VIA_PHONE
import re
from django.utils.translation import gettext_lazy as _

class SignUpForm(forms.ModelForm):
    email_phone_number = forms.CharField(label=_("Email yoki Telefon raqam"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Parol"))
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_("Parolni tasdiqlash"))

    class Meta:
        model = CustomUser
        fields = ["email_phone_number", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        user_input = cleaned_data.get("email_phone_number")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Parollar bir xil emas!"))

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        phone_regex = r'^\+?[0-9]{9,15}$'

        if not user_input:
            raise forms.ValidationError(_("Email yoki telefon raqam kiriting"))

        if re.match(email_regex, user_input):
            if CustomUser.objects.filter(email=user_input).exists():
                raise forms.ValidationError(_("Bu email allaqachon mavjud"))
            cleaned_data["auth_type"] = VIA_EMAIL
            cleaned_data["email"] = user_input

        elif re.match(phone_regex, user_input):
            if CustomUser.objects.filter(phone_number=user_input).exists():
                raise forms.ValidationError(_("Bu telefon raqam allaqachon mavjud"))
            cleaned_data["auth_type"] = VIA_PHONE
            cleaned_data["phone_number"] = user_input

        else:
            raise forms.ValidationError(_("Faqat email yoki telefon raqam kiriting"))

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_("Bu email allaqachon ro‘yxatdan o‘tgan"))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone_number=phone).exists():
            raise forms.ValidationError(_("Bu telefon raqam allaqachon ro‘yxatdan o‘tgan"))
        return phone

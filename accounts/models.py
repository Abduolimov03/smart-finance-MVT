from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
import random

VIA_EMAIL = "via_email"
VIA_PHONE = "via_phone"

class CustomUser(AbstractUser):
    email = models.EmailField(_("Email manzil"), unique=True, blank=True, null=True)
    phone_number = models.CharField(_("Telefon raqam"), max_length=13, unique=True, blank=True, null=True)
    auth_type = models.CharField(
        _("Autentifikatsiya turi"),
        max_length=20,
        choices=[(VIA_EMAIL, _("Email orqali")), (VIA_PHONE, _("Telefon orqali"))]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    def save(self, *args, **kwargs):
        if not self.username:
            if self.email:
                self.username = self.email
            elif self.phone_number:
                self.username = self.phone_number
            else:
                self.username = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email if self.email else self.phone_number

    def create_verify_code(self):
        """4 xonali tasdiqlash kodi yaratish"""
        return random.randint(1000, 9999)

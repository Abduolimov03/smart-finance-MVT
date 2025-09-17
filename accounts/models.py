from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
import random

VIA_EMAIL = "via_email"
VIA_PHONE = "via_phone"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    auth_type = models.CharField(max_length=20, choices=[(VIA_EMAIL, "Email"), (VIA_PHONE, "Phone")])

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
        return random.randint(1000, 9999)

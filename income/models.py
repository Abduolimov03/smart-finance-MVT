from django.conf import settings
from django.db import models

class Income(models.Model):
    PAYMENT_METHODS = [
        ('naqt', 'Naqd pul'),
        ('karta', 'Karta'),
        ('dollar', 'Dollar'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} {self.payment_method}"

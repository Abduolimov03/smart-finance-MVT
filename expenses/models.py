from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    PAYMENT_METHODS = [
        ('naqt', _('Naqt')),
        ('karta', _('Karta')),
        ('dollar', _('Dollar')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Foydalanuvchi")
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Nom")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Summasi")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name=_("To‘lov usuli")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Yaratilgan sana")
    )

    def __str__(self):
        return f"{self.title} - {self.amount} {self.payment_method}"

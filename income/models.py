from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Income(models.Model):
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
    title = models.CharField(max_length=255, verbose_name=_("Nom"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Summasi"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name=_("To‘lov usuli"))

    created_at = models.DateTimeField(
        verbose_name=_("Sana"),
        null=True,
        blank=True
    )

    USD_RATE = 12700  # dollar kursi

    def save(self, *args, **kwargs):
        if self.payment_method == "dollar":
            self.amount = self.amount * self.USD_RATE
            self.payment_method = "naqt"

        if not self.created_at:
            from django.utils.timezone import now
            self.created_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.amount} so'm"


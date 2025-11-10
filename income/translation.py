from modeltranslation.translator import register, TranslationOptions
from .models import Income

@register(Income)
class IncomeTranslationOptions(TranslationOptions):
    fields = ('title' , )

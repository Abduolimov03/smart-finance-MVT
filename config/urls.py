from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    # set_language URL POST so‘rovlari uchun
    path('set-language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('income/', include('income.urls')),
    path('expenses/', include('expenses.urls')),
)

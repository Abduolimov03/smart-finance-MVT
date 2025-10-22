import os
from pathlib import Path

# --- Asosiy loyihaning bazaviy papkasi ---
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Xavfsizlik sozlamalari ---
SECRET_KEY = "django-insecure-@aio75o7)gm05ife631gnl82u9laa9-=yk379&k0j_x0t6k)t9"
DEBUG = True
ALLOWED_HOSTS = []


# --- Django ilovalar ---
INSTALLED_APPS = [
    # Django standart app'lar
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Sizning app'laringiz
    "accounts",
    "income",
    "expenses",

    # Qo‘shimcha app'lar
    "django.contrib.humanize",
    "django.contrib.sites",

    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

SITE_ID = 1


# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Til almashtirish uchun
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --- URL va WSGI ---
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# --- Template sozlamalari ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # To‘g‘rilandi
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # allauth uchun zarur
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",  # i18n uchun
            ],
        },
    },
]


# --- Ma’lumotlar bazasi ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Parol validatori ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Til va vaqt sozlamalari ---
LANGUAGE_CODE = "uz"  # Asosiy til
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("uz", "O‘zbekcha"),
    ("ru", "Русский"),
    ("en", "English"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]


# --- Statik fayllar ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- Media fayllar ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# --- Email sozlamalari ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "asadbekabduolimov33@gmail.com"
EMAIL_HOST_PASSWORD = "yvzm bhhr htmq uven"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# --- Auth model va backend ---
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# --- Default model id turi ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

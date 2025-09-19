# Kirim-Chiqim Hisoblash Dasturi
Ushbu Django MVT loyihasi foydalanuvchining kirim va chiqimlarini boshqarish, balansni hisoblash va statistikalarni ko‘rsatish imkonini beradi.


## Funksiyalar
- Foydalanuvchi ro‘yxatdan o‘tishi va login qilish
- Kirim qo‘shish, tahrirlash, o‘chirish
- Chiqim qo‘shish, tahrirlash, o‘chirish
- Balans hisoblash (kunlik, haftalik, oylik, yillik)
- Kirim va chiqimlar grafigi (Chart.js)
- Vaqt oralig‘i bo‘yicha filtr
- Profilni boshqarish



## Texnologiyalar
- Python 3.12
- Django 5.x
- PostgreSQL (yoki SQLite)
- Chart.js (frontend grafigi uchun)
- HTML, CSS, JavaScript


## O‘rnatish
1. Loyihani klonlash:
   ```bash
   git clone https://github.com/username/kirim-chiqim-mvt.git
   cd kirim-chiqim-mvt
   


Virtual muhit yaratish:
python -m venv .env
source .env/bin/activate  # macOS/Linux
.env\Scripts\activate     # Windows

Kerakli paketlarni o‘rnatish:
pip install -r requirements.txt


.env faylini yaratish va sozlash:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost/dbname


Migratsiyalarni bajarish:
python manage.py migrate


Serverni ishga tushirish:
python manage.py runserver


Brauzerda ochish:
http://127.0.0.1:8000/

###  Foydalanish bo‘yicha tavsiyalar
```markdown
## Foydalanish
- Admin panelga kirish: `/admin/`
- Kirim qo‘shish: `/home/`
- Chiqim qo‘shish: `/expenses/`
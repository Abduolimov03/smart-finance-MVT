from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ProfileUpdateForm
from .models import CustomUser, VIA_EMAIL, VIA_PHONE
from .utils import generate_code, send_to_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from income.forms import IncomeForm
from income.models import Income
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum


@login_required
def home_view(request):
    form = IncomeForm(request.POST or None)

    # Yangi kirim qo‘shish
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        amount = form.cleaned_data["amount"]
        payment_method = form.cleaned_data["payment_method"]

        # Agar shunday kirim bo‘lsa, summani qo‘shish, aks holda yangi yozuv
        income_obj, created = Income.objects.filter(
            user=request.user,
            title=title,
            payment_method=payment_method
        ).first(), False

        if income_obj:
            income_obj.amount = F('amount') + amount
            income_obj.save()
        else:
            Income.objects.create(
                user=request.user,
                title=title,
                payment_method=payment_method,
                amount=amount
            )

        messages.success(request, "✅ Kirim qo‘shildi!")
        return redirect("home")

    # Foydalanuvchining barcha kirimlari
    incomes = Income.objects.filter(user=request.user).order_by("-created_at")

    # Umumiy summa
    total = incomes.aggregate(total_sum=Sum('amount'))['total_sum'] or 0

    # Kunlik, haftalik, oylik, yillik statistikalar
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())  # Dushanbadan
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)

    daily_total = incomes.filter(created_at__date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    weekly_total = incomes.filter(created_at__date__gte=start_week).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = incomes.filter(created_at__date__gte=start_month).aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_total = incomes.filter(created_at__date__gte=start_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Istalgan vaqt oralig‘i filtr
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            range_incomes = incomes.filter(
                created_at__date__gte=start_date_obj,
                created_at__date__lte=end_date_obj
            ).order_by('-created_at')
            range_total = range_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        except ValueError:
            range_incomes = []
            range_total = 0
    else:
        range_incomes = None
        range_total = None

    context = {
        "form": form,
        "incomes": incomes,
        "total": total,
        "daily_total": daily_total,
        "weekly_total": weekly_total,
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "range_incomes": range_incomes,
        "range_total": range_total,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "home.html", context)

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data["password"]

            user = CustomUser(
                auth_type=data.get("auth_type"),
                email=data.get("email"),
                phone_number=data.get("phone_number"),
            )
            user.set_password(password)
            user.is_active = False
            user.save()

            code = generate_code()
            request.session["verify_code"] = code
            request.session["verify_user"] = user.id

            if user.auth_type == VIA_EMAIL:
                send_to_mail(user.email, code)
                print(f"EMAIL CODE: {code}")

            elif user.auth_type == VIA_PHONE:
                print(f"PHONE CODE {user.phone_number}: {code}")

            messages.success(request, "Tasdiqlash kodi yuborildi, iltimos tasdiqlang!")
            return redirect("verify")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def verify_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        saved_code = str(request.session.get("verify_code"))
        user_id = request.session.get("verify_user")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi")
            return redirect("signup")

        if code == saved_code:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
            return redirect("home")
        else:
            messages.error(request, "Kod xato!")

    return render(request, "verify.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Email yoki parol noto‘g‘ri!")
            return redirect("login")

        if not user.is_active:
            messages.error(request, "Avval email yoki telefon raqamingizni tasdiqlang!")
            return redirect("verify")

        login(request, user)
        messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
        return redirect("home")

    return render(request, "login.html")




def forgot_password_view(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')

        if '@' in contact:
            try:
                user = CustomUser.objects.get(email=contact)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Bunday email mavjud emas')
                return redirect('forgot_password')
        else:
            try:
                user = CustomUser.objects.get(phone_number=contact)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Bunday telefon raqam mavjud emas')
                return redirect('forgot_password')

        code = random.randint(100000, 999999)
        request.session["reset_code"] = str(code)
        request.session["reset_user"] = user.id

        if user.email:
            send_mail(
                subject='Parolni tiklash kodi',
                message=f"Sizning parol tiklash kodingiz {code}",
                from_email=None,
                recipient_list=[user.email],

            )
            messages.success(request, "Emailingizga tasdiqlash kodi yuborildi!")
        else:
            print(f"Telefon raqam {user.phone_number}: {code}")
            messages.success(request, "Telefon raqamga tasdiqlash kodi yuborildi!")

        return redirect("reset_password")

    return render(request, "forgot_password.html")

def reset_password_view(request):
    if request.method == "POST":
        code = request.POST.get('code')
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "parollar mos emas")
            return redirect("reset_password")

        user_id = request.session.get("reset_user")
        seved_code = request.session.get("reset_code")

        if not user_id or not seved_code:
            messages.error(request, 'Avval kod oling')
            return redirect("forgot_password")

        if code != seved_code:
            messages.error(request, 'Code xato')
            return redirect('forgot_password')

        try:
            user = CustomUser.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, "parol yangilandi ")
            del request.session["reset_code"]
            del request.session["reset_user"]
            return redirect("login")
        except CustomUser.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi!")
            return redirect("forgot_password")

    return render(request, "reset_password.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Siz tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect("login")


@login_required
def change_profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma’lumotlari muvaffaqiyatli yangilandi!")
            return redirect("home")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "change_profile.html", {"form": form})
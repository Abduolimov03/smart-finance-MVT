from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login
from expenses.models import Expense
from .forms import SignUpForm, ProfileUpdateForm
from .models import CustomUser, VIA_EMAIL, VIA_PHONE
from .utils import generate_code, send_to_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from income.models import Income
from income.forms import IncomeForm
from django.db.models.functions import TruncDay, TruncMonth, TruncYear, TruncWeek
import json

login_required
def home_view(request):

    form = IncomeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        amount = form.cleaned_data["amount"]
        payment_method = form.cleaned_data["payment_method"]

        income_obj = Income.objects.filter(
            user=request.user,
            title=title,
            payment_method=payment_method
        ).first()

        if income_obj:
            income_obj.amount = F("amount") + amount
            income_obj.save()
        else:
            Income.objects.create(
                user=request.user,
                title=title,
                payment_method=payment_method,
                amount=amount,
            )

        messages.success(request, "Kirim qo‘shildi!")
        return redirect("home")

    incomes = Income.objects.filter(user=request.user).order_by("-created_at")
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")

    total_income = incomes.aggregate(total=Sum("amount"))["total"] or 0
    total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
    balance = total_income - total_expense

    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)

    daily_income = incomes.filter(created_at__date=today).aggregate(total=Sum("amount"))["total"] or 0
    weekly_income = incomes.filter(created_at__date__gte=start_week).aggregate(total=Sum("amount"))["total"] or 0
    monthly_income = incomes.filter(created_at__date__gte=start_month).aggregate(total=Sum("amount"))["total"] or 0
    yearly_income = incomes.filter(created_at__date__gte=start_year).aggregate(total=Sum("amount"))["total"] or 0

    period = request.GET.get("period", "day")
    if period == "week":
        trunc_func = TruncWeek
    elif period == "month":
        trunc_func = TruncMonth
    elif period == "year":
        trunc_func = TruncYear
    else:
        trunc_func = TruncDay

    income_chart = incomes.annotate(period=trunc_func("created_at")) \
                          .values("period") \
                          .annotate(total=Sum("amount")) \
                          .order_by("period")

    chart_labels = [entry["period"].strftime("%d-%m-%Y") for entry in income_chart]
    chart_values = [float(entry["total"]) for entry in income_chart]

    context = {
        "form": form,
        "incomes": incomes,
        "balance": balance,
        "daily_total": daily_income,
        "weekly_total": weekly_income,
        "monthly_total": monthly_income,
        "yearly_total": yearly_income,
        "chart_labels": json.dumps(chart_labels),
        "chart_values": json.dumps(chart_values),
        "period": period,
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
            messages.error(request, "Avval email yoki telefon raqamingizni tasdiqlan")
            return redirect("verify")

        login(request, user)
        messages.success(request, "Tizimga muvaffaqiyatli kirdingiz")
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
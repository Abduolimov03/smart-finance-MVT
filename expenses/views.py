from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, TruncMonth, TruncYear, TruncWeek
import json
from .forms import ExpenseForm
from income.models import Income
from .models import Expense


@login_required
def expense_home(request):
    form = ExpenseForm(request.POST or None)

    # Balansni hisoblash
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum("amount"))["total"] or 0
    balance = total_income - total_expenses

    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            amount = form.cleaned_data["amount"]
            payment_method = form.cleaned_data["payment_method"]

            # Mablag yetarliligi tekshiruvi
            if amount > balance:
                messages.error(request, f"❌ Hisobingizda mablag‘ yetarli emas! (Balans: {balance:,} so‘m)")
                return redirect("expense_home")

            # Title + payment_method bo'yicha tekshiradi
            expense_obj, created = Expense.objects.get_or_create(
                user=request.user,
                title=title,
                payment_method=payment_method,
                defaults={"amount": amount}
            )
            if not created:
                # Agar mavjud bo‘lsa, summasini qo‘shamiz
                expense_obj.amount = F("amount") + amount
                expense_obj.save(update_fields=["amount"])
                expense_obj.refresh_from_db()

            messages.success(request, "✅ Chiqim qo‘shildi!")
            return redirect("expense_home")
        else:
            messages.error(request, "❌ Iltimos, barcha maydonlarni to‘ldiring!")

    # Chiqimlar ro'yxati va statistikalar
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)

    daily_total = expenses.filter(created_at__date=today).aggregate(total=Sum("amount"))["total"] or 0
    weekly_total = expenses.filter(created_at__date__gte=start_week).aggregate(total=Sum("amount"))["total"] or 0
    monthly_total = expenses.filter(created_at__date__gte=start_month).aggregate(total=Sum("amount"))["total"] or 0
    yearly_total = expenses.filter(created_at__date__gte=start_year).aggregate(total=Sum("amount"))["total"] or 0

    # Sana oralig'i bo'yicha filtr
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    range_expenses, range_total = None, None
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            range_expenses = expenses.filter(
                created_at__date__gte=start_date_obj,
                created_at__date__lte=end_date_obj
            )
            range_total = range_expenses.aggregate(total=Sum("amount"))["total"] or 0
        except ValueError:
            messages.error(request, "Sana formati noto‘g‘ri!")

    # Grafik ma'lumotlar
    chart_data = expenses.annotate(day=TruncDay("created_at"))\
                         .values("day")\
                         .annotate(total=Sum("amount"))\
                         .order_by("day")
    chart_labels = [entry["day"].strftime("%d-%m-%Y") for entry in chart_data]
    chart_values = [float(entry["total"]) for entry in chart_data]

    context = {
        "form": form,
        "expenses": expenses,
        "total_expenses": total_expenses,
        "total_income": total_income,
        "balance": balance,
        "daily_total": daily_total,
        "weekly_total": weekly_total,
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "range_expenses": range_expenses,
        "range_total": range_total,
        "start_date": start_date,
        "end_date": end_date,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }

    return render(request, "home_content.html", context)

@login_required
def expense_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")

        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            payment_method=payment_method
        )
        return redirect('expense_home')

    return render(request, "add.html")

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, "Chiqim yangilandi!")
        return redirect("expense_home")
    return render(request, "expense_update.html", {"form": form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    messages.success(request, "Chiqim o‘chirildi!")
    return redirect("expense_home")


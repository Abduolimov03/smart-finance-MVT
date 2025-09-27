from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import IncomeForm
from .models import Income
from django.db.models import F
from django.utils.translation import gettext_lazy as _

@login_required
def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']

            if payment_method == "dollar":
                amount = amount * 12700
                payment_method = "naqt"

            incomes = Income.objects.filter(
                user=request.user,
                title=title,
                payment_method=payment_method
            )

            if incomes.exists():
                income_obj = incomes.first()
                income_obj.amount = F('amount') + amount
                income_obj.save()
                incomes.exclude(id=income_obj.id).delete()
            else:
                Income.objects.create(
                    user=request.user,
                    title=title,
                    payment_method=payment_method,
                    amount=amount
                )

            messages.success(request, _("Kirim qo‘shildi"))
            return redirect('home')
    else:
        form = IncomeForm()

    return render(request, 'income_add.html', {'form': form})


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'income_list.html', {'incomes': incomes})


@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, _("Kirim yangilandi"))
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income_update.html', {'form': form})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, _("Kirim o‘chirildi"))
        return redirect('income_list')
    return render(request, 'income_delete.html', {'income': income})

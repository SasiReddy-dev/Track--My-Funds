from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, datetime
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


# 🏠 HOME DASHBOARD
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    today = date.today()

    monthly_total = expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    category_totals = expenses.values('category') \
        .annotate(total=Sum('amount')) \
        .order_by('-total')

    highest_category = category_totals[0]['category'] if category_totals else 'N/A'

    context = {
        'expenses': expenses,
        'incomes': incomes,
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': balance,
        'monthly_total': monthly_total,
        'highest_category': highest_category,
    }

    return render(request, 'finance_app/home.html', context)


# ➕ ADD EXPENSE
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'finance_app/add_expense.html', {'form': form})


# ➕ ADD INCOME
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('home')
    else:
        form = IncomeForm()

    return render(request, 'finance_app/add_income.html', {'form': form})


# ❌ DELETE EXPENSE
@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('home')


# 📊 EXPENSE CHART
@login_required
def expense_chart(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    now = datetime.now()

    # ✅ safer conversion
    try:
        year = int(year) if year else now.year
    except:
        year = now.year

    try:
        month = int(month) if month else now.month
    except:
        month = now.month

    # ✅ USER FILTER FIX (IMPORTANT)
    expenses = Expense.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    category_data = expenses.values("category") \
        .annotate(total=Sum("amount")) \
        .order_by("-total")

    labels = [item["category"] for item in category_data]
    data = [float(item["total"]) for item in category_data]

    return render(request, "finance_app/expense_chart.html", {
        "labels": labels,
        "data": data,
        "current_month": f"{month:02d}",
        "current_year": year,
    })


# 📝 REGISTER
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)  # debug
    else:
        form = UserCreationForm()

    return render(request, 'finance_app/register.html', {'form': form})


# 🔐 LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'finance_app/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'finance_app/login.html')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')
# EDIT EXPENSE
@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'finance_app/edit_expense.html', {'form': form})
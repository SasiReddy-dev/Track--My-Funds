from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('expense-chart/', views.expense_chart, name='expense_chart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
]
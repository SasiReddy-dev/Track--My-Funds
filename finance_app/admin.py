from django.contrib import admin

from .models import Expense, Income

# Registering models to make them visible in Django Admin
admin.site.register(Expense)
admin.site.register(Income)


# Register your models here.

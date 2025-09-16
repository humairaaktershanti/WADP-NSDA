from django.contrib import admin
from .models import AddCash, Expense

@admin.register(AddCash)
class AddCashAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('source', 'description')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'amount', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('description',)
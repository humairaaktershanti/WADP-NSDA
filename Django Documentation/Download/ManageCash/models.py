from django.db import models
from django.contrib.auth.models import User

class AddCash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.source} - {self.amount}"
    
    class Meta:
        verbose_name = "Cash Entry"
        verbose_name_plural = "Cash Entries"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.amount}"
    
    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
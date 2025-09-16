from django.urls import path
from HrApp.views import *

urlpatterns = [
    path('categories/',Categories, name='Categories'),
    path('budgets/',budgets, name='budgets'),
    path('budget_expenses/',budget_expenses, name='budget_expenses'),
    path('budget_revenues/',budget_revenues, name='budget_revenues'),

    path('estimates/',estimates, name='estimates'),
    path('expenses/',expenses, name='expenses'),
    path('invoices/',invoices, name='invoices'),
    path('provident_fund/',provident_fund, name='provident_fund'),
    path('payments/',payments, name='payments'),
    path('taxes/',taxes, name='taxes'),

    path('salary/',salary, name='salary'),
    path('salary_view/',salary_view, name='salary_view'),
    path('payroll_items/',payroll_items, name='payroll_items'),

    path('policies/',policies, name='policies'),

    path('attendance_reports/',attendance_reports, name='attendance_reports'),
    path('daily_reports/',daily_reports, name='daily_reports'),
    path('employee_reports/',employee_reports, name='employee_reports'),
    path('expense_reports/',expense_reports, name='expense_reports'),
    path('invoice_reports/',invoice_reports, name='invoice_reports'),
    path('leave_reports/',leave_reports, name='leave_reports'),
    path('payments_reports/',payments_reports, name='payments_reports'),
    path('payslip_reports/',payslip_reports, name='payslip_reports'),
    path('project_reports/',project_reports, name='project_reports'),
    path('task_reports/',task_reports, name='task_reports'),
    path('user_reports/',user_reports, name='user_reports'),

]
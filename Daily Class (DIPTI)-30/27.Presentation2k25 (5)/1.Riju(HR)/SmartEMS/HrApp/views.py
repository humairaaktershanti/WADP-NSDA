from django.shortcuts import render

# Create your views here.
def Categories(request):
    return render(request, 'accounting/categories.html')

def budgets(request):
    return render(request, 'accounting/budgets.html')

def budget_revenues(request):
    return render(request, 'accounting/budget-revenues.html')

def budget_expenses(request):
    return render(request, 'accounting/budget-expenses.html')
# --------------------------Sales-----------------------
def estimates(request):
    return render(request, 'sales/estimates.html')

def payments(request):
    return render(request, 'sales/payments.html')

def expenses(request):
    return render(request, 'sales/expenses.html')

def invoices(request):
    return render(request, 'sales/invoices.html')

def provident_fund(request):
    return render(request, 'sales/provident-fund.html')

def taxes(request):
    return render(request, 'sales/taxes.html')

# --------------------------Payroll-----------------------
def salary(request):
    return render(request, 'payroll/salary.html')

def salary_view(request):
    return render(request, 'payroll/salary-view.html')

def payroll_items(request):
    return render(request, 'payroll/payroll-items.html')

# --------------------------Policies-----------------------
def policies(request):
    return render(request, 'policies.html')

# --------------------------Reports-----------------------
def attendance_reports(request):
    return render(request, 'reports/attendance-reports.html')

def daily_reports(request):
    return render(request, 'reports/daily-reports.html')

def employee_reports(request):
    return render(request, 'reports/employee-reports.html')

def expense_reports(request):
    return render(request, 'reports/expense-reports.html')

def invoice_reports(request):
    return render(request, 'reports/invoice-reports.html')

def leave_reports(request):
    return render(request, 'reports/leave-reports.html')

def payments_reports(request):
    return render(request, 'reports/payments-reports.html')

def payslip_reports(request):
    return render(request, 'reports/payslip-reports.html')

def project_reports(request):
    return render(request, 'reports/project-reports.html')

def task_reports(request):
    return render(request, 'reports/task-reports.html')

def user_reports(request):
    return render(request, 'reports/user-reports.html')
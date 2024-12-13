from django.contrib import admin
from .models import Employee, Salary, Position, PayrollPeriod, Deduction, WorkTime

admin.site.register(Employee)
admin.site.register(Salary)
admin.site.register(Position)
admin.site.register(PayrollPeriod)
admin.site.register(Deduction)
admin.site.register(WorkTime)
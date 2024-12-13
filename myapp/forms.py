from django import forms
from employees.models import Employee, Position

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'date_of_birth', 'hire_date', 'address', 'phone', 'email', 'telegram_id', 'position']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_title', 'base_salary']

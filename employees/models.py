from django.core.validators import MinValueValidator
from django.db import models

# Модель для Position (Посада)
class Position(models.Model):
    position_title = models.CharField(max_length=45)
    base_salary = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.position_title

# Модель для Employees (Працівники)
class Employee(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Telegram ID
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель для Work_Time (Робочий час)
class WorkTime(models.Model):
    work_date = models.DateField()
    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Work time for {self.employee.first_name} on {self.work_date}"

# Модель для Payroll_Periods (Платіжні періоди)
class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Payroll from {self.start_date} to {self.end_date}"

# Модель для Salaries (Зарплати)
class Salary(models.Model):
    base_salary = models.DecimalField(max_digits=9, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    bonuses = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)

    def __str__(self):
        return f"Salary for {self.employee.first_name} for period {self.payroll_period.start_date} to {self.payroll_period.end_date}"

# Модель для Deductions (Вирахування)
class Deduction(models.Model):
    deduction_type = models.CharField(max_length=45)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    deduction_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Deduction {self.deduction_type} for {self.employee.first_name} on {self.deduction_date}"

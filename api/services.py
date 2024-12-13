import random
from employees.models import Employee, WorkTime, Position, Deduction, Salary, PayrollPeriod
import concurrent.futures
import time
from django.db.models import F, Sum, Avg, FloatField
from django.db.models.functions import Cast


def fetch_random_employee_data():
    """Функція для отримання випадкових працівників з бази даних"""
    random_employee = random.choice(Employee.objects.all())
    return random_employee

def execute_parallel_queries(num_requests, num_threads):
    """Функція для виконання паралельних запитів д
    о бази даних"""
    # Вимірюємо час виконання
    start_time = time.time()

    # Створюємо пул потоків
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_requests):
            futures.append(executor.submit(fetch_random_employee_data))

        # Чекаємо, поки всі запити не будуть виконані
        concurrent.futures.wait(futures)

    end_time = time.time()

    # Повертаємо час виконання
    return end_time - start_time

import pandas as pd
from django.db.models import Sum, Avg, Count, F
from employees.models import Employee, Position, PayrollPeriod

# 1. Загальна кількість відпрацьованих годин кожного працівника
from django.db.models import F
def total_hours_by_employee(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['id', 'position', 'position__position_title']}
    queryset = (
        Employee.objects.filter(**valid_filters)
        .values('first_name', 'last_name', 'position__position_title')
        .annotate(
            total_hours_worked=Sum('worktime__hours_worked'),
            total_overtime_hours=Sum('worktime__overtime_hours')
        )
        .filter(total_hours_worked__gt=0)
        .order_by('-total_hours_worked')
    )
    df = pd.DataFrame.from_records(queryset)
    df['total_hours_worked'] = df['total_hours_worked'].fillna(0).astype(float)
    df['total_overtime_hours'] = df['total_overtime_hours'].fillna(0).astype(float)
    return df.to_dict('records')

# 2. Середня зарплата по кожній посаді
def average_salary_by_position(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['id', 'position_title']}
    queryset = (
        Position.objects.filter(**valid_filters)
        .values('position_title')
        .annotate(avg_salary=Avg('employee__salary'))
        .filter(avg_salary__gt=0)
        .order_by('-avg_salary')
    )
    df = pd.DataFrame.from_records(queryset)
    df['avg_salary'] = df['avg_salary'].fillna(0).astype(float)
    return df.to_dict('records')



# 3. Загальна сума вирахувань для кожного працівника
def total_deductions_by_employee(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['id', 'position', 'first_name', 'last_name']}
    queryset = (
        Employee.objects.filter(**valid_filters)
        .values('first_name', 'last_name')
        .annotate(total_deductions=Sum('deduction__amount'))
        .filter(total_deductions__gt=0)
        .order_by('-total_deductions')
    )

    # Перевірка, чи є результати
    if not queryset.exists():
        return []  # Повертаємо порожній список, якщо немає результатів

    df = pd.DataFrame.from_records(queryset)

    # Перевірка, чи є потрібний стовпець
    if 'total_deductions' not in df.columns:
        df['total_deductions'] = 0.0  # Додаємо стовпець із дефолтним значенням

    df['total_deductions'] = df['total_deductions'].fillna(0).astype(float)
    return df.to_dict('records')


# 4. Загальна сума зарплат за платіжними періодами
def total_salary_by_period(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['start_date', 'end_date', 'payment_date']}
    queryset = (
        PayrollPeriod.objects.filter(**valid_filters)
        .values('start_date', 'end_date')
        .annotate(
            total_salary=Sum(
                F('salary__base_salary') + F('salary__overtime_pay') + F('salary__bonuses')
            )
        )
        .filter(total_salary__gt=0)
        .order_by('-total_salary')
    )
    df = pd.DataFrame.from_records(queryset)
    df['total_salary'] = df['total_salary'].fillna(0).astype(float)
    return df.to_dict('records')


# 5. Середня кількість годин роботи по кожному працівнику
def average_work_hours_by_employee(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['first_name', 'last_name', 'position']}
    queryset = (
        Employee.objects.filter(**valid_filters)
        .values('first_name', 'last_name')
        .annotate(
            avg_hours_worked=Avg('worktime__hours_worked'),
            avg_overtime_hours=Avg('worktime__overtime_hours')
        )
        .filter(avg_hours_worked__gt=0)
        .order_by('-avg_hours_worked')
    )
    df = pd.DataFrame.from_records(queryset)
    df['avg_hours_worked'] = df['avg_hours_worked'].astype(float)
    df['avg_overtime_hours'] = df['avg_overtime_hours'].astype(float)
    return df.to_dict('records')


def positions_with_max_deductions(filters=None):
    filters = filters or {}
    valid_filters = {k: v for k, v in filters.items() if k in ['id', 'position_title']}
    queryset = (
        Position.objects.filter(**valid_filters)
        .values('position_title')
        .annotate(total_deductions=Sum('employee__deduction__amount'))
        .filter(total_deductions__gt=0)
        .order_by('-total_deductions')
    )
    df = pd.DataFrame.from_records(queryset)
    df['total_deductions'] = df['total_deductions'].fillna(0).astype(float)
    return df.to_dict('records')


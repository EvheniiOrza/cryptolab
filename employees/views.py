from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .models import Position, Employee, WorkTime, PayrollPeriod, Salary, Deduction
from .serializers import (
    PositionSerializer,
    EmployeeSerializer,
    WorkTimeSerializer,
    PayrollPeriodSerializer,
    SalarySerializer,
    DeductionSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg, Sum, Count, F
from django.db.models.functions import TruncMonth
from employees.models import Position

def employee_by_telegram_id(request, telegram_id):
    try:
        employee = Employee.objects.get(telegram_id=telegram_id)
        salary = Salary.objects.filter(employee=employee).first()
        total_salary = salary.base_salary + salary.bonuses + salary.overtime_pay

        return render(request, 'employees/employee_detail.html', {
            'employee': employee,
            'salary': salary,
            'total_salary': total_salary
        })
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)


@api_view(['GET'])
def employee_by_telegram_id_user(request, telegram_id):
    employee = get_object_or_404(Employee, telegram_id=telegram_id)
    serializer = EmployeeSerializer(employee)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    return Response(serializer.data)



class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkTimeViewSet(viewsets.ModelViewSet):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PayrollPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def report(self, request):
        aggregated_data = Salary.objects.aggregate(
            total_base_salary=Sum('base_salary'),
            total_overtime_pay=Sum('overtime_pay'),
            total_bonuses=Sum('bonuses'),
        )
        return Response(aggregated_data)

# 1. Загальна кількість годин роботи працівників за місяць
total_hours_per_month = (
    WorkTime.objects.annotate(month=TruncMonth('work_date'))
    .values('month')
    .annotate(total_hours=Sum('hours_worked'))
    .order_by('month')
)

# 2. Середня зарплата за посадами
average_salary_by_position = (
    Position.objects.annotate(average_salary=Avg('employee__salary__base_salary'))
    .values('position_title', 'average_salary')
    .order_by('-average_salary')
)

# 3. Загальна сума бонусів по кожному працівнику
total_bonuses_by_employee = (
    Employee.objects.annotate(total_bonuses=Sum('salary__bonuses'))
    .values('first_name', 'last_name', 'total_bonuses')
    .order_by('-total_bonuses')
)

# 4. Співвідношення базової зарплати до понаднормових (групування за працівниками)
base_to_overtime_ratio = (
    Salary.objects.annotate(
        ratio=F('base_salary') / (F('overtime_pay') + 1)  # Уникаємо ділення на 0
    )
    .values('employee__first_name', 'employee__last_name', 'ratio')
    .order_by('-ratio')
)

# 5. Кількість працівників за типами вирахувань
deductions_by_type = (
    Deduction.objects.values('deduction_type')
    .annotate(total_employees=Count('employee', distinct=True))
    .order_by('-total_employees')
)

# 6. Сумарна зарплата по платіжним періодам
total_salary_by_period = (
    PayrollPeriod.objects.annotate(
        total_salary=Sum('salary__base_salary')
    )
    .values('start_date', 'end_date', 'total_salary')
    .order_by('start_date')
)

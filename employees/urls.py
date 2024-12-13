from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PositionViewSet,
    EmployeeViewSet,
    WorkTimeViewSet,
    PayrollPeriodViewSet,
    SalaryViewSet,
    DeductionViewSet,
)

router = DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'worktimes', WorkTimeViewSet)
router.register(r'payrollperiods', PayrollPeriodViewSet)
router.register(r'salaries', SalaryViewSet)
router.register(r'deductions', DeductionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employee/telegram/<str:telegram_id>/', views.employee_by_telegram_id, name='employee_by_telegram_id'),
]



from bokeh.embed import components
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from employees.models import Employee, WorkTime, Salary, Deduction


# Create your views here.


def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Використовуємо форму з полем telegram_id

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Зберігаємо користувача
            user = form.save(commit=False)
            user.save()

            # Отримуємо telegram_id із форми
            telegram_id = form.cleaned_data.get('telegram_id')

            # Створюємо пов'язаний об'єкт Employee
            Employee.objects.create(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                telegram_id=telegram_id,
                position=None,  # За замовчуванням (можливо, треба додати логіку для вибору посади)
                hire_date=None  # За замовчуванням
            )

            return redirect('login')  # Перенаправлення до логіну
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render
import plotly.express as px
from bokeh.plotting import figure

def plotly_dashboard(request):
    # Example data
    data = {'Employees': ['John', 'Doe', 'Alice'], 'Hours Worked': [160, 150, 170]}
    fig = px.bar(data, x='Employees', y='Hours Worked', title='Work Hours')
    graph = fig.to_html(full_html=False)
    return render(request, 'dashboard_v1.html', {'graph': graph})

def bokeh_dashboard(request):
    # Example data
    plot = figure(title="Employee Overtime", x_axis_label='Employees', y_axis_label='Hours')
    plot.vbar(x=['John', 'Doe', 'Alice'], top=[10, 15, 20], width=0.5, color="navy")
    script, div = components(plot)
    return render(request, 'dashboard_v2.html', {'script': script, 'div': div})


from django.shortcuts import render, get_object_or_404, redirect
from employees.models import Employee, WorkTime, Salary, Deduction


def profile(request):
    user = request.user
    try:
        # Спробуйте знайти співпадіння за telegram_id або email
        employee = Employee.objects.get(telegram_id=user.username)
    except Employee.DoesNotExist:
        try:
            employee = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            # Якщо співпадінь не знайдено, перенаправляємо на головну
            return redirect('home')

    # Отримуємо дані для профілю
    work_times = WorkTime.objects.filter(employee=employee)
    salaries = Salary.objects.filter(employee=employee)
    deductions = Deduction.objects.filter(employee=employee)

    return render(request, 'profile.html', {
        'employee': employee,
        'work_times': work_times,
        'salaries': salaries,
        'deductions': deductions,
    })



from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from employees.models import Employee

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            telegram_id=instance.username,  # Прив'язуємо telegram_id до username
        )

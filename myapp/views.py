from django.http import JsonResponse

from .NetworkHelper import NetworkHelper
from django.shortcuts import render, get_object_or_404, redirect
from employees.models import Employee, Position
from .forms import EmployeeForm, PositionForm
network_helper = NetworkHelper(base_url="http://127.0.0.1:9500/myapp/api", username="user1", password="123321A10")
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
import json

def client_list(request):
    clients = network_helper.get_list()  # Отримання списку клієнтів
    return render(request, "myapp/clients_list.html", {"clients": clients})

def get_client(request, client_id):
    client = network_helper.get_item_by_id(client_id)  # Отримання клієнта за ID
    return render(request, "myapp/client_detail.html", {"client": client})

def create_client(request):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "registration_date": request.POST.get("registration_date"),
        }
        network_helper.create_item(data)
        return redirect("client_list")
    return render(request, "myapp/create_client.html")
def update_client(request, client_id):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "registration_date": request.POST.get("registration_date"),
        }
        network_helper.update_item_by_id(client_id, data)
        return redirect("client_list")

    client = network_helper.get_item_by_id(client_id)
    return render(request, "myapp/update_client.html", {"client": client})
def delete_client(request, client_id):
    if request.method == "POST":
        network_helper.delete_item_by_id(client_id)
        return redirect("client_list")



# Список працівників
def employee_list(request):
    if request.headers.get('Accept') == 'application/json':
        print("Returning JSON response")  # Додаємо лог для JSON
        employees = Employee.objects.all().values('id', 'first_name', 'last_name', 'position__position_title')
        return JsonResponse(list(employees), safe=False)
    else:
        print("Rendering HTML response")  # Лог для HTML
        employees = Employee.objects.all()
        return render(request, 'employees/employee_list.html', {'employees': employees})


# Деталі працівника
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.headers.get('Accept') == 'application/json':
        data = {
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': employee.position.position_title
        }
        return JsonResponse(data)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@csrf_exempt
def api_employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        data = {
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': employee.position.position_title,
        }
        return JsonResponse(data)
    except Employee.DoesNotExist:
        error_data = {'error': 'Employee not found'}
        return JsonResponse(error_data, status=404)

# Додавання працівника
@csrf_exempt
def employee_create(request):
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)

            form = EmployeeForm(data)
            if form.is_valid():
                employee = form.save()
                return JsonResponse({'id': employee.id, 'message': 'Employee created successfully'}, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('employee_list')
    else:
        form = EmployeeForm()
        return render(request, 'employees/employee_form.html', {'form': form})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
# Редагування працівника
@csrf_exempt
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)

            form = EmployeeForm(data, instance=employee)
            if form.is_valid():
                updated_employee = form.save()
                return JsonResponse({'id': updated_employee.id, 'message': 'Employee updated successfully'}, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee)
        return render(request, 'employees/employee_form.html', {'form': form})
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Видалення працівника
@csrf_exempt
def employee_delete(request, pk):
    # Перевірка чи метод DELETE
    if request.method == 'DELETE':
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully'}, status=204)  # Використовуємо статус 204
    return JsonResponse({'error': 'Invalid request method'}, status=400)
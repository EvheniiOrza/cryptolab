# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),               # List clients
    path('client/<int:client_id>/', views.get_client, name='get_client'), # View single client
    path('create/', views.create_client, name='create_client'),     # Create client
    path('update/<int:client_id>/', views.update_client, name='update_client'), # Update client
    path('delete/<int:client_id>/', views.delete_client, name='delete_client'), # Delete client

    path('list/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.api_employee_detail, name='employee_detail'),
    path('employee_by_id/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/add/', views.employee_create, name='employee_add'),
    path('employee/<int:pk>/edit/', views.employee_update, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
]

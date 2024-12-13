# In api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_v1/', views.plotly_dashboard, name='dashboard_v1'),
    path('dashboard_v2/', views.bokeh_dashboard, name='dashboard_v2'),
    path('test_parallel_queries/', views.test_parallel_queries, name='test_parallel_queries'),
]

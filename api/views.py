import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components

from .forms import DashboardFilterForm
from .services import (  # Імпортуємо нові функції
    total_hours_by_employee,
    average_salary_by_position,
    total_salary_by_period,
    average_work_hours_by_employee,
    positions_with_max_deductions,
    total_deductions_by_employee,
)
def plotly_dashboard(request):
    # Ініціалізація форми
    form = DashboardFilterForm(request.GET or None)

    # Отримання фільтрів
    filters = {}
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    position = request.GET.get('position')

    if start_date and end_date:
        filters['employee__deduction__deduction_date__range'] = (start_date, end_date)

    if position:
        filters['id'] = position

    # Застосування фільтрів до функцій
    employee_data = total_hours_by_employee()
    avg_salary_by_position = average_salary_by_position(filters)
    total_salary_by_period_data = total_salary_by_period(filters)
    avg_work_hours = average_work_hours_by_employee(filters)
    positions_with_max_deductions_data = positions_with_max_deductions(filters)
    total_deductions_data = total_deductions_by_employee()
    # Обробка даних для графіків
    df_employee = pd.DataFrame(employee_data)
    fig1 = px.bar(df_employee, x='first_name', y='total_hours_worked', title="Години роботи працівників")

    df_salary = pd.DataFrame(avg_salary_by_position)
    fig2 = px.bar(df_salary, x='position_title', y='avg_salary', title="Середня зарплата по посадах")

    df_salary_period = pd.DataFrame(total_salary_by_period_data)
    fig3 = px.line(df_salary_period, x='start_date', y='total_salary', title="Загальна зарплата за періоди")

    df_work_hours = pd.DataFrame(avg_work_hours)
    fig4 = px.bar(df_work_hours, x='first_name', y='avg_hours_worked', title="Середні години роботи працівників")

    df_deductions = pd.DataFrame(positions_with_max_deductions_data)
    fig5 = px.pie(df_deductions, names='position_title', values='total_deductions', title="Вирахування по позиціях")

    df_total_deductions = pd.DataFrame(total_deductions_data)

    if df_total_deductions.empty:
        print("df_total_deductions is empty")
    else:
        print("df_total_deductions columns:", df_total_deductions.columns)
        print("df_total_deductions preview:", df_total_deductions.head())

    fig6 = px.bar(df_total_deductions, x='first_name', y='total_deductions', title="Загальна сума вирахувань")

    # Відображення графіків у шаблоні
    graphs = [fig1.to_html(), fig2.to_html(), fig3.to_html(), fig4.to_html(), fig5.to_html(), fig6.to_html()]

    return render(request, 'dashboard_v1.html', {
        'graphs': graphs,
        'form': form,
    })

def bokeh_dashboard(request):
    # Ініціалізація форми
    form = DashboardFilterForm(request.GET or None)

    # Отримання фільтрів
    filters = {}
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    position = request.GET.get('position')

    if start_date and end_date:
        filters['employee__deduction__deduction_date__range'] = (start_date, end_date)

    if position:
        filters['id'] = position

    # Застосування фільтрів до функцій
    employee_data = total_hours_by_employee()
    avg_salary_by_position = average_salary_by_position(filters)
    total_salary_by_period_data = total_salary_by_period(filters)
    avg_work_hours = average_work_hours_by_employee(filters)
    positions_with_max_deductions_data = positions_with_max_deductions(filters)
    total_deductions_data = total_deductions_by_employee()

    # Перетворення даних у DataFrame
    df_employee = pd.DataFrame(employee_data)
    df_salary = pd.DataFrame(avg_salary_by_position)
    df_salary_period = pd.DataFrame(total_salary_by_period_data)
    df_work_hours = pd.DataFrame(avg_work_hours)
    df_deductions = pd.DataFrame(positions_with_max_deductions_data)
    df_total_deductions = pd.DataFrame(total_deductions_data)

    # Створення графіків з Bokeh
    source1 = ColumnDataSource(df_employee)
    p1 = figure(x_range=df_employee['first_name'].tolist(), title="Години роботи працівників", x_axis_label="Ім'я",
                y_axis_label="Години", height=350, width=600)
    p1.vbar(x='first_name', top='total_hours_worked', width=0.9, source=source1)

    source2 = ColumnDataSource(df_salary)
    p2 = figure(x_range=df_salary['position_title'].tolist(), title="Середня зарплата по посадах", x_axis_label="Посада",
                y_axis_label="Зарплата", height=350, width=600)
    p2.vbar(x='position_title', top='avg_salary', width=0.9, source=source2)

    source3 = ColumnDataSource(df_salary_period)
    p3 = figure(x_range=df_salary_period['start_date'].astype(str).tolist(), title="Загальна зарплата за періоди",
                x_axis_label="Дата", y_axis_label="Зарплата", height=350, width=600)
    p3.line(x='start_date', y='total_salary', source=source3, line_width=2)

    source4 = ColumnDataSource(df_work_hours)
    p4 = figure(x_range=df_work_hours['first_name'].tolist(), title="Середні години роботи", x_axis_label="Ім'я",
                y_axis_label="Години", height=350, width=600)
    p4.vbar(x='first_name', top='avg_hours_worked', width=0.9, source=source4)

    source5 = ColumnDataSource(df_deductions)
    p5 = figure(x_range=df_deductions['position_title'].tolist(), title="Вирахування по позиціях", x_axis_label="Посада",
                y_axis_label="Вирахування", height=350, width=600)
    p5.vbar(x='position_title', top='total_deductions', width=0.9, source=source5)

    if not df_total_deductions.empty:
        source6 = ColumnDataSource(df_total_deductions)
        p6 = figure(x_range=df_total_deductions['first_name'].tolist(), title="Загальна сума вирахувань", x_axis_label="Ім'я",
                    y_axis_label="Вирахування", height=350, width=600)
        p6.vbar(x='first_name', top='total_deductions', width=0.9, source=source6)
    else:
        p6 = None

    # Генерація скриптів і HTML-дивів для шаблону
    graphs = [
        components(p1),
        components(p2),
        components(p3),
        components(p4),
        components(p5),
    ]

    if p6:
        graphs.append(components(p6))

    # Повернення графіків у шаблон
    return render(request, 'dashboard_v2.html', {
        'graphs': graphs,
        'form': form,
    })


import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render
from .services import execute_parallel_queries, fetch_random_employee_data

def test_parallel_queries(request):
    """
    Дашборд для тестування паралельних запитів з використанням функції fetch_random_employee_data.
    """
    # Параметри для тестування
    num_requests_list = [50, 100, 150]  # Кількість запитів
    num_threads_list = [1, 2, 4, 8, 16]  # Кількість потоків

    results = []

    # Виконуємо експерименти для різних кількостей запитів і потоків
    for num_requests in num_requests_list:
        for num_threads in num_threads_list:
            # Викликаємо execute_parallel_queries з функцією fetch_random_employee_data
            time_taken = execute_parallel_queries(num_requests, num_threads)
            results.append((num_requests, num_threads, time_taken))

    # Побудова графіку
    fig, ax = plt.subplots(figsize=(10, 6))
    for num_requests in num_requests_list:
        filtered_results = [result for result in results if result[0] == num_requests]
        num_threads = [result[1] for result in filtered_results]
        times = [result[2] for result in filtered_results]
        ax.plot(num_threads, times, label=f'{num_requests} запитів')

    ax.set_xlabel('Кількість потоків')
    ax.set_ylabel('Час виконання (секунди)')
    ax.set_title('Час виконання запитів в залежності від кількості потоків і запитів')
    ax.legend()

    # Зберігаємо графік в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Відображаємо графік на сторінці
    return render(request, 'test_parallel_queries.html', {'graph': img_str})

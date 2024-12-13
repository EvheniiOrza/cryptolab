import requests
import pandas as pd

# Отримання даних
response = requests.get('http://localhost:8000/api/salaries/average_salary/')
data = response.json()
df = pd.DataFrame(data)

# Базовий аналіз
mean_salary = df['average_salary'].mean()
median_salary = df['average_salary'].median()
min_salary = df['average_salary'].min()
max_salary = df['average_salary'].max()

print(f"Середня: {mean_salary}, Медіана: {median_salary}, Мінімум: {min_salary}, Максимум: {max_salary}")

from concurrent.futures import ThreadPoolExecutor
import requests

# Функція для отримання даних
def fetch_data(api_url):
    response = requests.get(api_url)
    return response.json()

# API-ендпоїнти
urls = [
    'http://localhost:8000/api/salaries/average_salary/',
    'http://localhost:8000/api/work_hours/total_hours/',
]

# Використання багатопотоковості
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_data, urls))

print(results)

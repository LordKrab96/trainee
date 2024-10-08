import pandas as pd
import json
import os
from datetime import datetime

# 1. Считываем данные из файла
data = pd.read_csv('test_data.csv', sep=';')

# 2. Заполняем пропущенные значения
data.ffill(inplace=True)

# 3. Добавляем минимум, максимум и средние значения
temperature_min = data['temperature'].min()
temperature_max = data['temperature'].max()
temperature_mean = data['temperature'].mean()

utilization_min = data['utilization'].min()
utilization_max = data['utilization'].max()
utilization_mean = data['utilization'].mean()

data['min_temperature'] = temperature_min
data['max_temperature'] = temperature_max
data['mean_temperature'] = temperature_mean

data['min_utilization'] = utilization_min
data['max_utilization'] = utilization_max
data['mean_utilization'] = utilization_mean

# 4. Добавляем статус
def determine_status(row):
    if (row['temperature'] > temperature_mean + 0.3 * temperature_max) or \
       (row['utilization'] > utilization_mean + 0.3 * utilization_max):
        return 'WARNING'
    return 'OK'

data['status'] = data.apply(determine_status, axis=1)

# 5. Сортируем данные по возрастанию timestamp
data.sort_values(by='timestamp', inplace=True)

# Удаление ненужного столбца (если есть)
if 'Unnamed: 0' in data.columns:
    data.drop(columns=['Unnamed: 0'], inplace=True)

# 6. Сохраняем данные в файлы
timestamp_now = datetime.now().strftime("%d%m%Y_%H%M%S")
json_filename = f'{timestamp_now}.json'
csv_filename = f'{timestamp_now}.csv'

data.to_json(json_filename, orient='records', lines=True)
data.to_csv(csv_filename, index=True)

print(f'Data saved to {json_filename} and {csv_filename}')

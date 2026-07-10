import requests

# Ваш реальный рабочий адрес
URL = "https://bot.globalinstore.ru:8001/endpoint"

# Передаем данные напрямую через параметр json=
# Библиотека requests сама правильно преобразует словарь в JSON и выставит заголовки
payload = {"key": "Проверка связи через HTTPS"}

print("Отправка запроса...")
try:
    response = requests.post(URL, json=payload, timeout=5)
    print("Статус-код ответа:", response.status_code)
    print("Ответ от FastAPI:", response.json())
except Exception as e:
    print("Произошла ошибка при тесте:", e)

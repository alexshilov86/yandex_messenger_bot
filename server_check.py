import requests

# 1. Укажите IP-адрес вашего сервера и порт
# Если проверяете на том же сервере: используйте 'http://127.0.0.1:8000'
# Если проверяете из сети: укажите реальный IP сервера, например 'http://95.213.x.x:8000'
SERVER_URL = "https://bot.globalinstore.ru/" # 

def test_server():
    print("--- Шаг 1: Проверка GET-запроса (получение списка сообщений) ---")
    try:
        get_response = requests.get(f"{SERVER_URL}/messages", timeout=5)
        print(f"Статус ответа: {get_response.status_code}")
        print(f"Данные с сервера: {get_response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}\n")
        return

    print("--- Шаг 2: Проверка POST-запроса (отправка нового сообщения) ---")
    payload = {
        "sender": "Python-Тестер",
        "text": "Привет! Это проверочное сообщение через requests.",
        "priority": "high"
    }
    
    try:
        post_response = requests.post(f"{SERVER_URL}/messages", json=payload, timeout=5)
        print(f"Статус ответа: {post_response.status_code} (Ожидалось: 201)")
        print(f"Ответ сервера: {post_response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке: {e}\n")
        return

    print("--- Шаг 3: Повторный GET-запрос (проверяем, сохранилось ли сообщение) ---")
    final_response = requests.get(f"{SERVER_URL}/messages")
    print(f"Текущие сообщения на сервере: {final_response.json()}")

if __name__ == "__main__":
    test_server()

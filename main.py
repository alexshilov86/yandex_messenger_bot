import requests

# URL-адрес API Яндекс Мессенджера для отправки текста
url = "https://botapi.messenger.yandex.net/bot/v1/messages/sendText/"

# Заголовки запроса (авторизация и тип контента)
headers = {
    "Authorization": "OAuth y0__wgBEOK5hvoIGJaREyCI1IKXGCZ-TzV1lOeL4Oek0EK-fGA7r-xb",
    "Content-Type": "application/json"
}

# Тело запроса с данными получателя и текстом
payload = {
    "login": "avshilov995@yandex.ru",
    "text": "Привет!"
}

# Выполнение POST-запроса
response = requests.post(url, json=payload, headers=headers)

# Вывод ответа от сервера Яндекса в формате JSON
print(response.json())
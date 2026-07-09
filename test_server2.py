import requests

URL = "https://bot.globalinstore.ru/webhook"

payload = {
    "update_type": "message",
    "message": {
        "text": "Тест из test_webhook.py",
        "chat": {"id": "test-chat-2"},
        "sender": {"id": "user-123"}
    }
}

resp = requests.post(URL, json=payload, verify=False, timeout=10)
print("Status code:", resp.status_code)
print("Response:", resp.text)

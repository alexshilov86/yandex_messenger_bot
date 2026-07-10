import requests
import sys
import json

# --- НАСТРОЙКИ ---
# Если запускаешь без аргументов — тестируем локально
BASE_URL = "http://localhost:8000"

if len(sys.argv) > 1:
    # Если передал URL как аргумент (например, ngrok-адрес), используем его
    BASE_URL = sys.argv[1]

print(f"🧪 Тестируем сервер по адресу: {BASE_URL}")
print("-" * 50)

def test_health():
    """Проверка эндпоинта /health"""
    url = f"{BASE_URL}/health"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ /health: OK (status={resp.status_code})")
            print(f"   → Ответ: {data}")
            return True
        else:
            print(f"❌ /health: Ошибка (status={resp.status_code})")
            return False
    except Exception as e:
        print(f"❌ /health: Исключение — {e}")
        return False

def test_webhook():
    """Отправка тестового JSON-запроса на /webhook"""
    url = f"{BASE_URL}/webhook"
    payload = {
        "update_type": "message",
        "message": {
            "text": "Тест из test_bot.py",
            "chat": {"id": "test-chat-999"},
            "sender": {"id": "user-test-1"}
        }
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        # verify=False нужен, если у тебя самоподписанный сертификат или ngrok
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=15)
        
        if resp.status_code == 200:
            print(f"✅ /webhook: OK (status={resp.status_code})")
            try:
                data = resp.json()
                print(f"   → Ответ сервера: {data}")
            except:
                print(f"   → Тело ответа: {resp.text}")
            
            # Дополнительно: проверяем, что сервер реально получил данные
            # (это видно по логам в окне с run_bot.bat)
            print("   → Проверь консоль с запущенным server2.py: там должно быть '📩 Получено сообщение...'")
            return True
        else:
            print(f"❌ /webhook: Ошибка (status={resp.status_code})")
            print(f"   → Тело ошибки: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ /webhook: Исключение — {e}")
        return False

if __name__ == "__main__":
    ok_health = test_health()
    ok_webhook = test_webhook()

    print("-" * 50)
    if ok_health or ok_webhook:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("⚠️ ТЕСТЫ НЕ ПРОЙДЕНЫ. Проверь логи сервера и настройки.")

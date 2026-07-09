from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Получаем тело запроса как JSON
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Для отладки можно вывести payload в лог
    # print(payload)

    # Извлекаем нужные поля (структура зависит от версии API — сверяйте с документацией)
    update_type = payload.get("update_type")
    if update_type != "message":
        # Игнорируем другие типы обновлений, если не нужны
        return {"status": "ok"}

    message = payload.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")
    sender_id = message.get("sender", {}).get("id")

    if not chat_id:
        return {"status": "ok"}  # или вернуть ошибку, если критично

    # --- ЗДЕСЬ ВАША ЛОГИКА БОТА ---
    response_text = f"Вы написали: {text}"

    # Отправка ответа через API Яндекс Мессенджера (пример)
    # В реальном проекте вынесите токен в переменные окружения
    import requests
    BOT_TOKEN = "y0__wgBEOK5hvoIGJaREyCI1IKXGCZ-TzV1lOeL4Oek0EK-fGA7r-xb"
    SEND_TEXT_URL = "https://botapi.messenger.yandex.net/bot/v1/messages/sendText"

    send_payload = {
        "chat_id": chat_id,
        "text": response_text
    }

    headers = {
        "Authorization": f"OAuth {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    resp = requests.post(SEND_TEXT_URL, json=send_payload, headers=headers, timeout=10)
    if resp.status_code != 200:
        # Логируйте ошибку, не отдавайте детали наружу
        print(f"Send error: {resp.status_code} {resp.text}")

    return {"status": "ok"}

if __name__ == "__main__":
    # Запуск для локальной проверки (на сервере используйте gunicorn/uvicorn как сервис)
    uvicorn.run(app, host="0.0.0.0", port=8000)

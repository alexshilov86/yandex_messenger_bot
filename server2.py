import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
load_dotenv()

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# --- ТОКЕН (НЕ ХРАНИ В КОДЕ!) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: Переменная окружения BOT_TOKEN не задана!")
    raise RuntimeError("BOT_TOKEN is required. Set it in env or .bat")

SEND_TEXT_URL = "https://botapi.messenger.yandex.net/bot/v1/messages/sendText"


@app.get("/health")
def health():
    """Проверка доступности сервера (можно открыть в браузере)."""
    return {"status": "ok", "domain": "bot.globalinstore.ru"}


@app.post("/webhook")
async def handle_webhook(request: Request):
    # Парсим JSON
    try:
        payload = await request.json()
    except Exception as e:
        logger.warning(f"Invalid JSON: {e}")
        return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid JSON"})

    # Обрабатываем только сообщения
    if payload.get("update_type") != "message":
        return {"status": "ok"}

    message = payload.get("message", {})
    text = message.get("text", "")
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    sender = message.get("sender") or {}
    sender_id = sender.get("id")

    if not chat_id:
        logger.warning("No chat_id in payload")
        return {"status": "ok"}

    logger.info(f"📩 Получено сообщение: chat_id={chat_id}, sender_id={sender_id}, text={text}")

    # --- ТВОЯ БИЗНЕС-ЛОГИКА ЗДЕСЬ ---
    # Сюда можно вставить функции для Яндекс/Google Таблиц, API ПЭК, координат и т.д.
    response_text = process_message(text, chat_id, sender_id)
    # --------------------------------

    # Отправляем ответ ботом
    send_payload = {"chat_id": chat_id, "text": response_text}
    headers = {
        "Authorization": f"OAuth {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(SEND_TEXT_URL, json=send_payload, headers=headers, timeout=10)
        if resp.status_code != 200:
            logger.error(f"❌ Ошибка отправки сообщения: status={resp.status_code}, body={resp.text}")
        else:
            logger.info(f"✅ Сообщение отправлено в chat_id={chat_id}")
    except Exception as e:
        logger.exception(f"❌ Исключение при отправке сообщения: {e}")

    # Важно: вебхук всегда должен вернуть 200 OK Яндексу, даже если отправка не удалась
    return {"status": "ok"}


def process_message(text: str, chat_id: str, sender_id: str) -> str:
    """
    Здесь твоя логика: команды, таблицы, API доставки и т.п.
    """
    # Примеры команд
    if text.strip().lower() in ["/start", "привет", "start"]:
        return "Привет! Я бот. Напиши адрес — посчитаю доставку."

    # Пример обработки команды с адресом (для интеграции с таблицами/API)
    if text.lower().startswith("/адрес "):
        address = text[len("/адрес "):].strip()
        # Здесь можно вызвать: get_coords(address), get_price_from_sheet(coords), и т.д.
        return f"Ты указал адрес: {address}. (Здесь будет расчёт доставки)"

    return f"Вы написали: {text}"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

app = FastAPI(title="Message Receiver API")

# 1. Описываем объект "from" (Отправитель)
class UserFrom(BaseModel):
    id: str
    login: str
    display_name: str

# 2. Описываем объект "chat" (Чат)
class Chat(BaseModel):
    id: str
    type: str
    title: Optional[str] = None  # Имя чата может быть пустым в некоторых типах чатов

# 3. Переписываем структуру "message"
class Message(BaseModel):
    message_id: int
    from_user: UserFrom = Field(..., alias="from")  # Маппим зарезервированное слово 'from' в 'from_user'
    chat: Chat
    timestamp: int
    text: str

    # Включаем поддержку работы с алиасами (для корректного чтения JSON)
    class Config:
        populate_by_name = True

# 4. Главный корневой объект, который приходит на сервер
class Update(BaseModel):
    update_id: int
    message: Message


# Очередь в памяти для хранения последних 10 сообщений
received_messages_db = []

# Меняем тип входящих данных в эндпоинте с Message на Update
@app.post("/messages", status_code=201)
async def receive_message(update: Update):
    msg = update.message  # Достаем объект сообщения для удобства
    
    # Валидация (если текст пустой)
    if not msg.text.strip():
        raise HTTPException(status_code=420, detail="Текст сообщения не может быть пустым")
    
    # Конвертируем timestamp из секунд в читаемую дату
    readable_time = datetime.fromtimestamp(msg.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    full_message_data = {
        "update_id": update.update_id,
        "timestamp": readable_time,
        "sender_name": msg.from_user.display_name,
        "sender_login": msg.from_user.login,
        "text": msg.text,
        "chat_id": msg.chat.id
    }
    
    # Красивый вывод в консоль сервера
    print(f"[{readable_time}] От {msg.from_user.display_name} ({msg.from_user.login}): {msg.text}")
    
    # Сохраняем в наш временный список
    received_messages_db.append(full_message_data)
    if len(received_messages_db) > 10:
        received_messages_db.pop(0)
        
    return {"status": "accepted", "message_id": msg.message_id}

@app.get("/messages")
async def get_messages():
    return {"messages": received_messages_db}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(title="Message Receiver API")

# Описываем модель входящего сообщения
class Message(BaseModel):
    sender: str = Field(..., example="Система Мониторинга")
    text: str = Field(..., example="Внимание! На сервере заканчивается место.")
    priority: str = Field(default="normal", example="high")

# Очередь в памяти для хранения последних 10 сообщений (для примера)
received_messages_db = []

@app.post("/messages", status_code=201)
async def receive_message(msg: Message):
    # Простая валидация (если текст пустой)
    if not msg.text.strip():
        raise HTTPException(status_code=420, detail="Текст сообщения не может быть пустым")
    
    # Добавляем системные данные (время приема)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message_data = {
        "timestamp": timestamp,
        "sender": msg.sender,
        "text": msg.text,
        "priority": msg.priority
    }
    
    # Выводим в консоль сервера
    print(f"[{timestamp}] [{msg.priority.upper()}] От {msg.sender}: {msg.text}")
    
    # Сохраняем в наш временный список
    received_messages_db.append(full_message_data)
    if len(received_messages_db) > 10:
        received_messages_db.pop(0) # Храним только последние 10
        
    return {"status": "accepted", "message_id": len(received_messages_db)}

# Дополнительный маршрут, чтобы можно было посмотреть принятые сообщения
@app.get("/messages")
async def get_messages():
    return {"messages": received_messages_db}

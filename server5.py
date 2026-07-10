from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn  # Импортируем uvicorn

app = FastAPI()

class Data(BaseModel):
    key: str

@app.post("/endpoint")
def handle_data(item: Data):
    return {"status": "success", "received": item.key}

# Этот блок сработает, только если запускать файл напрямую
if __name__ == "__main__":
    uvicorn.run(
        "server:app",  # Замените 'server', если ваш файл называется по-другому
        host="0.0.0.0",
        port=8000,     # Внутренний порт, который слушает IIS/роутер
        ssl_certfile=r"C:\Certbot\live\bot.globalinstore.ru\fullchain.pem",
        ssl_keyfile=r"C:\Certbot\live\bot.globalinstore.ru\privkey.pem"
    )

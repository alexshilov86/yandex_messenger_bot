import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Инициализируем приложение FastAPI
app = FastAPI(title="Мой первый API сервер")


# Описываем структуру данных, которую мы ожидаем получить в POST-запросе
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


# 1. Простой GET-запрос (например, проверка работы сервера)
@app.get("/")
def read_root():
    return {"message": "Сервер успешно запущен и доступен по сети!"}


# 2. GET-запрос с параметром в URL (динамический путь)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "status": "Найден"}


# 3. POST-запрос для отправки данных (принимает JSON-тело)
@app.post("/items/")
def create_item(item: Item):
    return {
        "status": "Данные успешно получены",
        "received_data": item.dict(),
    }


# Точка входа для запуска файла напрямую через Python
if __name__ == "__main__":
    # host="0.0.0.0" позволяет серверу принимать внешние и локальные сетевые запросы.
    # port=8000 — стандартный порт для разработки.
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

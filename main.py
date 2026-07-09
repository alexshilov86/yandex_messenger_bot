from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def handle_post(request: Request):
    # Получаем данные в формате JSON
    data = await request.json()
    print(f"Получен JSON: {data}")
    return {"status": "success", "payload": data}

if __name__ == "__main__":
    import uvicorn
    # Запуск на внутреннем порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

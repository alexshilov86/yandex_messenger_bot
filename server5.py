from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    key: str

@app.post("/endpoint")
def handle_data(item: Data):
    return {"status": "success", "received": item.key}

from fastapi import FastAPI


app = FastAPI(title="Сервис бронирования столиков")

@app.get("/")
async def root():
    return {"message": "Сервис бронирования столиков"}
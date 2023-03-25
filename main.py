from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as register_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["mongodb+srv://evertonmedeiros:4kXWUncAHXuUjW4S@cluster0.yoxdzl7.mongodb.net/?retryWrites=true&w=majority"])
    app.database = app.mongodb_client[config["BancoTeste"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(register_router, tags=["books"], prefix="/book")


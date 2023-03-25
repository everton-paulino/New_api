from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as register_router

app = FastAPI()
config = dotenv_values(".env")
app.include_router(register_router, tags=["register"], prefix="/register")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["mongodb+srv://evertonmedeiros:4kXWUncAHXuUjW4S@cluster0.yoxdzl7.mongodb.net/?retryWrites=true&w=majority"])
    app.database = app.mongodb_client[config["BancoTeste"] + "test"]

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("register")

def test_create_register():
    with TestClient(app) as client:
        response = client.post("/register/", json={"name": "Don Quixote", "cpf": "767.633.970-70", "createAt": "25/03/2023"})
        assert response.status_code == 201

        body = response.json()
        assert body.get("name") == "Don Quixote"
        assert body.get("cpf") == "767.633.970-70"
        assert body.get("createAt") == "25/03/2023"
        assert "_id" in body


def test_create_register_missing_name():
    with TestClient(app) as client:
        response = client.post("/register/", json={"cpf": "767.633.970-70", "createAt": "25/03/2023"})
        assert response.status_code == 422


def test_create_register_missing_cpf():
    with TestClient(app) as client:
        response = client.post("/register/", json={"name": "Don Quixote", "createAt": "25/03/2023"})
        assert response.status_code == 422


def test_create_register_missing_createAt():
    with TestClient(app) as client:
        response = client.post("/register/", json={"name": "Don Quixote", "cpf": "767.633.970-7"})
        assert response.status_code == 422


def test_get_register():
    with TestClient(app) as client:
        new_book = client.post("/register/", json={"name": "Don Quixote", "cpf": "767.633.970-7", "createAt": "25/03/2023"}).json()

        get_book_response = client.get("/register/" + new_register.get("_id"))
        assert get_register_response.status_code == 200
        assert get_register_response.json() == new_book


def test_get_register_unexisting():
    with TestClient(app) as client:
        get_register_response = client.get("/register/unexisting_id")
        assert get_register_response.status_code == 404


def test_update_register():
    with TestClient(app) as client:
        new_register = client.post("/register/", json={"name": "Don Quixote", "cpf": "767.633.970-7", "createAt": "25/03/2023"}).json()

        response = client.put("/register/" + new_register.get("_id"), json={"name": "Don Quixote 1"})
        assert response.status_code == 200
        assert response.json().get("name") == "Don Quixote 1"


def test_update_register_unexisting():
    with TestClient(app) as client:
        update_register_response = client.put("/register/unexisting_id", json={"name": "Don Quixote 1"})
        assert update_register_response.status_code == 404


def test_delete_register():
    with TestClient(app) as client:
        new_register = client.post("/register/", json={"name": "Don Quixote", "cpf": "767.633.970-7", "createAt": "25/03/2023"}).json()

        delete_register_response = client.delete("/register/" + new_register.get("_id"))
        assert delete_register_response.status_code == 204


def test_delete_register_unexisting():
    with TestClient(app) as client:
        delete_register_response = client.delete("/register/unexisting_id")
        assert delete_register_response.status_code == 404


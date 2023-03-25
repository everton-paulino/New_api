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
        response = client.post("/register/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Don Quixote"
        assert body.get("author") == "Miguel de Cervantes"
        assert body.get("synopsis") == "..."
        assert "_id" in body


def test_create_register_missing_title():
    with TestClient(app) as client:
        response = client.post("/register/", json={"author": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 422


def test_create_register_missing_author():
    with TestClient(app) as client:
        response = client.post("/register/", json={"title": "Don Quixote", "synopsis": "..."})
        assert response.status_code == 422


def test_create_register_missing_synopsis():
    with TestClient(app) as client:
        response = client.post("/register/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_get_register():
    with TestClient(app) as client:
        new_book = client.post("/register/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        get_book_response = client.get("/register/" + new_register.get("_id"))
        assert get_register_response.status_code == 200
        assert get_register_response.json() == new_book


def test_get_register_unexisting():
    with TestClient(app) as client:
        get_register_response = client.get("/register/unexisting_id")
        assert get_register_response.status_code == 404


def test_update_book():
    with TestClient(app) as client:
        new_register = client.post("/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        response = client.put("/register/" + new_register.get("_id"), json={"title": "Don Quixote 1"})
        assert response.status_code == 200
        assert response.json().get("title") == "Don Quixote 1"


def test_update_register_unexisting():
    with TestClient(app) as client:
        update_register_response = client.put("/register/unexisting_id", json={"title": "Don Quixote 1"})
        assert update_register_response.status_code == 404


def test_delete_register():
    with TestClient(app) as client:
        new_register = client.post("/book/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        delete_register_response = client.delete("/book/" + new_register.get("_id"))
        assert delete_register_response.status_code == 204


def test_delete_register_unexisting():
    with TestClient(app) as client:
        delete_register_response = client.delete("/book/unexisting_id")
        assert delete_register_response.status_code == 404


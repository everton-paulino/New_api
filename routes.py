from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import register, registerUpdate

router = APIRouter()

@router.post("/", response_description="Create a new register", status_code=status.HTTP_201_CREATED, response_model=register)
def create_register(request: Request, register: register = Body(...)):
    register = jsonable_encoder(register)
    new_register = request.app.database["registers"].insert_one(register)
    created_register = request.app.database["registers"].find_one(
        {"_id": new_register.inserted_id}
    )

    return created_register


@router.get("/", response_description="List all registers", response_model=List[register])
def list_registers(request: Request):
    registers = list(request.app.database["registers"].find(limit=100))
    return registers


@router.get("/{id}", response_description="Get a single register by id", response_model=register)
def find_register(id: str, request: Request):
    if (register := request.app.database["registers"].find_one({"_id": id})) is not None:
        return register

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"register with ID {id} not found")


@router.put("/{id}", response_description="Update a register", response_model=register)
def update_register(id: str, request: Request, register: registerUpdate = Body(...)):
    register = {k: v for k, v in register.dict().items() if v is not None}

    if len(register) >= 1:
        update_result = request.app.database["registers"].update_one(
            {"_id": id}, {"$set": register}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"register with ID {id} not found")

    if (
        existing_register := request.app.database["registers"].find_one({"_id": id})
    ) is not None:
        return existing_register

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"register with ID {id} not found")


@router.delete("/{id}", response_description="Delete a register")
def delete_register(id: str, request: Request, response: Response):
    delete_result = request.app.database["registers"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"register with ID {id} not found")

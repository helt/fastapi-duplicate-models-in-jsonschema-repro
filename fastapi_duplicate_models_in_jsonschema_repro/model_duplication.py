from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel, Field


class PetBase(BaseModel):
    name: str = "Unnamed pet"
    petType: str


class Pet(PetBase):
    id: UUID = Field(default_factory=lambda: uuid4())


# register startup event
@asynccontextmanager
async def lifespan(application: FastAPI):
    dump_openapi(application)
    yield


# Init FastAPI and connect routers
app = FastAPI(debug=True, lifespan=lifespan, )


@app.get("/pets")
async def pets() -> List[Pet]:
    return [
        Pet(name="Felix", petType="cat"),
        Pet(name="Kitty", petType="cat"),
        Pet(name="Wolf", petType="dog"),
        Pet(name="Rex", petType="dog"),
    ]


@app.post("/")
async def create(payload: PetBase) -> Pet:
    pet = Pet(**payload.model_dump())
    return pet


@app.put("/")
async def update(pet: Pet) -> Pet:
    pet.name = pet.name + " update"
    return pet


def dump_openapi(application: FastAPI):
    target = Path("build/openapi.json")
    os.makedirs("build", exist_ok=True)
    if application.openapi() is not None:
        with open(target, "w") as f:
            json.dump(application.openapi(), f, sort_keys=True, indent=True)

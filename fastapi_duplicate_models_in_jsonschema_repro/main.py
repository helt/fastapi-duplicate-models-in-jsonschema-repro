from contextlib import asynccontextmanager
from enum import Enum
import json
import os
from pathlib import Path
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel, Field

class PetType(str, Enum):
    CAT = "cat"
    DOG = "dog"


class Pet(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = "Unnamed pet"
    petType: str

class HuntingSkill(Enum):
    CLUELESS = "clueless"
    LAZY = "lazy"
    ADVENTUROUS = "adventurous"
    AGGRESSIVE = "aggressive"

class Cat(Pet):
    petType: Literal[PetType.CAT] = PetType.CAT
    huntingSkill: Annotated[HuntingSkill, Field( default=HuntingSkill.LAZY, description="The measured skill for hunting")]

class Dog(Pet):
    petType: Literal[PetType.DOG] = PetType.DOG
    packSize: Annotated[int, Field(format="int32", minimum=0, default=0)]

Cohort = Annotated[Union[Dog, Cat], Field(..., discriminator="petType")]

# register startup event
@asynccontextmanager
async def lifespan(application: FastAPI):
    dump_openapi(application)
    yield

# Init FastAPI and connect routers
app = FastAPI(debug=True, lifespan=lifespan)

@app.get("/") 
async def list() -> List[Pet]:
    return [Cat(name="Felix"), Cat(name="Kitty"), Dog(name="Wolf"), Dog(name="Rex")]

@app.post("/")
async def update(foo: Pet) -> Pet:
    foo.id = uuid4()

@app.get("/get_cat")
async def get_cat(q: str) -> Cat:
    return Cat(name=q)

@app.get("/get_dog")
async def get_dog(q: str) -> Dog:
    return Dog(name=q)

def dump_openapi(application: FastAPI):
    target = Path("build/openapi.json")
    os.makedirs("build", exist_ok=True)
    if application.openapi() is not None:
        with open(target, 'w') as f:
            json.dump(application.openapi(), f, sort_keys=True, indent=True)

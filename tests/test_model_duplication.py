import json
from typing import List
from fastapi.testclient import TestClient
from pydantic import RootModel

from fastapi_duplicate_models_in_jsonschema_repro.model_duplication import (
    Pet,
    PetBase,
    app,
)

client = TestClient(app)


# PetList = RootModel[List[Pet]]
class PetList(RootModel):
    root: List[Pet]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


def create_pet():
    expected = PetBase(name="Foobar", petType="bar")
    print(expected.model_dump_json())
    response = client.post("/", expected.model_dump_json())
    assert 200 <= response.status_code < 300
    r = response.json()
    pet = Pet.model_validate(r)
    assert pet.name == expected.name
    assert pet.petType == expected.petType
    assert pet.id is not None


def test_list_pets():
    response = client.get("/pets")
    assert response.status_code == 200
    r = response.json()
    # how to parse into the corresponding Cat/Dog class based on the discriminator automatically?
    parsed = PetList.model_validate(r)

    # unwrap that damn thing
    pets = [x for x in parsed]

    assert len(pets) == 4
    cat = pets[0]

    assert cat.petType == "cat"
    assert cat.name == "Felix"

    assert isinstance(cat, Pet)


def test_pydantic_inheritance_name():
    schema = Pet.model_json_schema()
    assert "id" in schema["properties"]
    assert schema["properties"]["id"] == {
        "format": "uuid",
        "title": "Id",
        "type": "string",
    }
    assert "name" not in schema["properties"]
    assert "allOf" in schema


def test_pydantic_inheritance_PetBase_as_expected():
    schema = PetBase.model_json_schema()
    assert schema == {
        "properties": {
            "name": {"default": "Unnamed pet", "title": "Name", "type": "string"},
            "petType": {"title": "Pettype", "type": "string"},
        },
        "required": ["petType"],
        "title": "PetBase",
        "type": "object",
    }


def test_pydantic_inheritance_Pet_allOf_with_PetBase():
    schema = Pet.model_json_schema()
    assert schema == {
        "allOf": [
            {"$ref": "#/components/schemas/PetBase"},
            {
                "type": "object",
                "properties": {
                    "id": {"format": "uuid", "title": "Id", "type": "string"}
                },
                "required": ["id"],
            },
        ]
    }

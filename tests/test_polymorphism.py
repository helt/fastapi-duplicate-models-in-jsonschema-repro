from fastapi.testclient import TestClient

from fastapi_duplicate_models_in_jsonschema_repro.polymorphism import (
    Cat,
    Pet,
    Dog,
    app,
    PetType,
)

client = TestClient(app)


def test_read_main():
    response = client.get("/get_cat?q=flix")
    assert response.status_code == 200
    r = response.json()
    cat = Cat.model_validate(r)
    assert cat.name == "flix"


def test_list_pets():
    response = client.get("/pets")
    assert response.status_code == 200
    r = response.json()
    # how to parse into the corresponding Cat/Dog class based on the discriminator automatically?
    parsed = [Pet(**x) for x in r]
    cat = parsed[0]

    assert len(parsed) == 4
    assert cat.petType == PetType.CAT

    assert isinstance(cat, Pet)
    assert isinstance(cat, Cat)
    assert isinstance(cat, Dog) is False

from fastapi.testclient import TestClient

from fastapi_duplicate_models_in_jsonschema_repro.main import Cat, Pet, PetType, app

client = TestClient(app)


# def test_read_main():
#     response = client.get("/get_cat?q=flix")
#     assert response.status_code == 200
#     r = response.json()
#     cat = Cat(**r)
#     assert cat.name == "flix"


def test_list_pets():
    response = client.get("/")
    assert response.status_code == 200
    r = response.json()
    parsed = [Pet(**x) for x in r]

    assert len(parsed) == 4
    assert parsed[0].petType == PetType.CAT
    

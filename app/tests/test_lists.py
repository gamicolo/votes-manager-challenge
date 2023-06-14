from app.tests.conftest import app
from app.database.crud.lists import lists_crud
from fastapi.testclient import TestClient
from app.config import settings

def test_get_all_lists_with_valid_election_id(set_all_lists, client):
    election_id=1
    expected_lists=['A','B']

    response = client.get(f"/lists/{election_id}")

    assert response.json() == expected_lists
    assert response.status_code == 200

def test_get_all_lists_with_invalid_election_id(client):
    election_id=10
    expected_detail_string = 'No lists for the id 10 were found on the system'

    response = client.get(f"/lists/{election_id}")

    assert response.json()['detail'] == expected_detail_string
    assert response.status_code == 404

#TODO modificar la validacion para identificar cuando no esta creada la elecion del caso de la listas vacias para una elecion
def test_get_empty_lists_with_valid_election_id(set_empty_lists, client):
    election_id=1
    expected_lists=['A','B']

    response = client.get(f"/lists/{election_id}")

    print(response.json())

    #assert response.json() == expected_lists
    #assert response.status_code == 200

#### PUT /lists/
def test_post_create_valid_list(set_empty_lists, client):
    election_id=1
    expected_list_name='A'

    response = client.post(f"/lists",json={'election_id':election_id, 'name':expected_list_name})

    assert response.json()['name'] == expected_list_name
    assert response.status_code == 200

def test_update_list_name_of_valid_election(set_all_lists, client):
    election_id=1
    expected_list_name='A'

    response = client.post(f"/lists",json={'election_id':election_id, 'name':expected_list_name})

    assert response.json()['name'] == expected_list_name
    assert response.status_code == 200

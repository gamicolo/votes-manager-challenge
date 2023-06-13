from app.tests.conftest import app
from app.database.crud.votes import votes_crud
from fastapi.testclient import TestClient
from app.config import settings

#GET
def test_get_all_votes_of_lists_with_valid_election_id(set_lists_with_votes, client):
    election_id=1
    expected_votes=[{'A': 10}, {'B': 5}, {'C': 20}, {'D': 0}, {'E': 10}]

    response = client.get(f"/votes/{election_id}")

    assert response.json()[0]['A'] == 10
    assert response.json()[1]['B'] == 5
    assert response.json()[2]['C'] == 20
    assert response.json()[3]['D'] == 0
    assert response.json()[4]['E'] == 10
    assert response.status_code == 200

#GET
def test_get_all_votes_of_lists_with_invalid_election_id(client):
    election_id=10
    expected_detail_string = 'No lists for the id 10 were found on the system'

    response = client.get(f"/lists/{election_id}")

    assert response.json()['detail'] == expected_detail_string
    assert response.status_code == 404

##TODO modificar la validacion para identificar cuando no esta creada la elecion del caso de la listas vacias para una elecion
def test_get_empty_lists_with_valid_election_id(set_empty_lists, client):
    pass

#POST
def test_create_valid_votes_of_list(set_lists_without_votes, client):
    election_id=1
    list_name='A'
    votes_A=10

    response = client.post(f"/votes",json={'election_id':election_id, 'list_name':list_name, 'votes': votes_A})

    assert response.json()['election_id'] == election_id
    assert response.json()['list_name'] == list_name
    assert response.json()['votes'] == votes_A
    assert response.status_code == 200

##PUT
#def test_update_votes_of_valid_election(set_lists_with_votes, client):
#    election_id=1
#    list_name='A'
#    votes_A=15
#
#    response = client.put(f"/votes",json={'election_id':election_id, 'list_name':list_name, 'votes': votes_A})
#
#    print(response.json())
#
#    #assert response.json()['election_id'] == election_id
#    #assert response.json()['list_name'] == list_name
#    #assert response.json()['votes'] == votes_A
#    #assert response.status_code == 200

from app.tests.conftest import app
from app.database.crud.elections import elections_crud
from app.config import settings

#### GET
def test_get_number_of_seats_from_valid_election(set_election, client):
    num_of_seats=50
    election_id=1
    response = client.get(f"/elections/{election_id}")

    assert response.json() == num_of_seats
    assert response.status_code == 200

def test_get_number_of_seats_from_invalid_election(client):
    election_id=100
    expected_detail_string = f'No seats assigned for the election with id {election_id} were found on the system'

    response = client.get(f"/elections/{election_id}")

    assert response.json()['detail'] == expected_detail_string
    assert response.status_code == 404

def test_get_seats_distribution_from_funciton_valid_election(set_lists_with_votes_for_elections_result, client):
    election_id=1

    response = client.get(f"/elections/{election_id}/results")

    assert response.json().get('A') == 3
    assert response.json().get('B') == 3
    assert response.json().get('C') == 1
    assert response.json().get('D') == 0
    assert response.json().get('E') == 0
    assert response.status_code == 200

def test_get_seats_distribution_from_db_valid_election(set_election_with_seats_distribution, client):
    election_id=1

    response = client.get(f"/elections/{election_id}/results")

    assert response.json().get('A') == 2
    assert response.json().get('B') == 1
    assert response.json().get('C') == 0
    assert response.status_code == 200

#### POST 
def test_create_election_and_store_number_of_seats_success(client):
    num_of_seats=50
    election_id=1

    response = client.post("/elections", json={'seats': num_of_seats})
    
    assert response.status_code == 200
    assert response.json()['id'] == election_id
    assert response.json()['seats'] == num_of_seats
    assert response.json()['seats_distribution'] == {}

def test_create_election_without_seats_parameter(set_election, client):
    election_id=1
    num_of_seats=10
    expected_detail_string = "Missing parameter 'seats' on request body or its imcomplete"

    response = client.post("/elections")

    assert response.json()['detail'] == expected_detail_string
    assert response.status_code == 422

#### PUT
def test_store_elections_result_success(set_election, client):
    num_of_seats=50
    election_id=1
    seats_distribution={'A':10, 'B':5, 'C': 0}

    response = client.put(f"/elections/{election_id}/results", json={'seats_distribution': seats_distribution})
    
    assert response.status_code == 200
    assert response.json()['id'] == election_id
    assert response.json()['seats'] == num_of_seats
    assert response.json()['seats_distribution'].get('A') == 10
    assert response.json()['seats_distribution'].get('B') == 5
    assert response.json()['seats_distribution'].get('C') == 0

def test_update_number_of_seats_for_valid_elections(set_election, client):
    num_of_seats=10
    election_id=1

    response = client.put(f"/elections/{election_id}", json={'seats': num_of_seats})

    #print(response.json())
    
    assert response.status_code == 200
    assert response.json()['id'] == election_id
    assert response.json()['seats'] == num_of_seats
    assert response.json()['seats_distribution'] == {}

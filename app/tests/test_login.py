from app.tests.conftest import app
from app.services import login as login_services
from app.config import settings
from app.database.schemas.login import UserInDB
from app.database.models.login import User as UserModel

#from fastapi.testclient import TestClient
from fastapi import HTTPException
from jose import jwt

#### Services
#def test_get_user(db_with_user):
    #TODO

def test_get_user_with_user_not_in_db(db):

    username='johndoe'
    user=login_services.get_user(db, username)

    assert user == None

#def test_verify_password(client):
#    pass
#def test_get_password_hash(client):
#    pass
#

def test_create_access_token():

    first_jwt = login_services.create_access_token(data={'sub':'johndoe'})
    second_jwt = login_services.create_access_token(data={'sub':'jhondoe'})
    
    assert first_jwt is not second_jwt

def test_create_access_token_for_user(dummy_user):

    token = login_services.create_access_token(data={'sub': dummy_user.username})
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['sub'] == dummy_user.username
    
def test_authenticate_user_success(mocker,dummy_user):

    username='johndoe'
    password='12345678'
    hashed_password=login_services.pwd_context.hash(password)

    mocker.patch('app.services.login.get_user', return_value=dummy_user)

    user_in_db = login_services.authenticate_user(mocker, username, password)

    assert user_in_db.username == 'johndoe'


#def test_authenticate_user_user_in_db(db_with_user):
#
#    username='johndoe'
#    password='12345678'
#    hashed_password=login_services.pwd_context.hash(password)
#
#    user_in_db = login_services.authenticate_user(db_with_user, username, password)
#
#    assert user_in_db.username == 'johndoe'


def test_authenticate_user_not_user_in_db(mocker):

    username='johndoe'
    password='12345678'
    mocker.patch('app.services.login.get_user', return_value=None)

    user_in_db = login_services.authenticate_user(mocker, username, password)

    assert user_in_db == False


###### Routes
def test_login_for_access_token(mocker,dummy_user,client):

    mocker.patch('app.services.login.get_user', return_value=dummy_user)

    form_data = {
        "username": "johndoe",
        "password": "12345678"
    }
    response = client.post(  
        "/login", 
        data=form_data,
        headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
    )

    result = response.json()

    assert result['access_token'] is not None
    assert result['token_type'] == 'bearer'

def test_login_for_access_token_with_no_user_on_db(mocker,client):

    mocker.patch('app.services.login.get_user', return_value=None)
    form_data = {
        "username": "johndoe",
        "password": "12345678"
    }
    response = client.post(  
        "/login", 
        data=form_data,
        headers={ 'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 401
    assert response.json()['detail'] == "Incorrect username or password"

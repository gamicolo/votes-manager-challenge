import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from fastapi import FastAPI
from app.database.crud.elections import elections_crud
from app.database.crud.lists import lists_crud
from app.database.crud.votes import votes_crud

from app.router.main_router import router
from app.database.dbbase import Base

from app.dependencies import get_db
from app.dependencies import db_session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(router)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    db_session.set(db)
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c

@pytest.fixture
def set_election(db):
    db_session.set(db)
    elections_crud.create(50)

@pytest.fixture
def set_all_lists(db):
    db_session.set(db)
    elections_crud.create(50)
    lists_crud.create(1,'A')
    lists_crud.create(1,'B')

@pytest.fixture
def set_empty_lists(db):
    db_session.set(db)
    elections_crud.create(50)

@pytest.fixture
def set_lists_with_votes(db):
    db_session.set(db)
    elections_crud.create(5)
    lists_crud.create(1,'A')
    lists_crud.create(1,'B')
    lists_crud.create(1,'C')
    lists_crud.create(1,'D')
    lists_crud.create(1,'E')
    votes_crud.create(1,'A',10)
    votes_crud.create(1,'B',5)
    votes_crud.create(1,'C',20)
    votes_crud.create(1,'D',0)
    votes_crud.create(1,'E',10)

@pytest.fixture
def set_lists_without_votes(db):
    db_session.set(db)
    elections_crud.create(5)
    lists_crud.create(1,'A')
    lists_crud.create(1,'B')
    lists_crud.create(1,'C')
    lists_crud.create(1,'D')
    lists_crud.create(1,'E')

@pytest.fixture
def set_lists_with_votes_for_elections_result(db):
    db_session.set(db)
    elections_crud.create(7)
    lists_crud.create(1,'A')
    lists_crud.create(1,'B')
    lists_crud.create(1,'C')
    lists_crud.create(1,'D')
    lists_crud.create(1,'E')
    votes_crud.create(1,'A',340000)
    votes_crud.create(1,'B',280000)
    votes_crud.create(1,'C',160000)
    votes_crud.create(1,'D',60000)
    votes_crud.create(1,'E',15000)

@pytest.fixture
def set_election_with_seats_distribution(db):
    db_session.set(db)
    elections_crud.create(3,{'A':2, 'B':1, 'C':0})

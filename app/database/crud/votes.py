from sqlalchemy.orm import Session, load_only
from app.dependencies import db_session
from app.database.models.elections import Elections as ElectionsModel
from app.database.models.lists import Lists as ListsModel
from app.database.models.votes import Votes as VotesModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class VotesCRUD():

    def create(self, election_id: int, list_name: str, votes: int):

        """
        Create/Load the votes for a specific list
        """

        db = db_session.get()
        if not (db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()):
            raise NotFoundOnDBException

        list_row = db.query(ListsModel).filter(ListsModel.name == list_name).first()
        if not (list_row):
            raise NotFoundOnDBException

        db_votes = VotesModel( election_id=election_id, list_name=list_row.name, votes=votes )
        db.add(db_votes)
        db.commit()
        db.refresh(db_votes)

        return db_votes

    def get_all_votes(self, election_id: int):
        """
        Get all votes for all the lists from a specific election
        """

        db = db_session.get()
        db_rows = db.query(VotesModel).filter(VotesModel.election_id == election_id).options(load_only('list_name', 'votes')).all()
        if not db_rows:
            raise NotFoundOnDBException

        return {row.list_name: row.votes for row in db_rows}

    #TODO evaluar si se debera quitar este metodo
    def update(self, election_id: int, list_name: str, votes: int):
        """
        Update the amount of votes of a specific list of the election
        """

        db = db_session.get()
        if not (db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()):
            raise NotFoundOnDBException

        list_row = db.query(ListsModel).filter(ListsModel.name == list_name).first()
        if not (list_row):
            raise NotFoundOnDBException

        db_votes = VotesModel( election_id=election_id, list_name=list_row.name, votes=votes )
        db.add(db_votes)
        db.commit()
        db.refresh(db_votes)

        return db_votes

votes_crud = VotesCRUD()


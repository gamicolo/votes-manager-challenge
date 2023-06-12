from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.elections import Elections as ElectionsModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class ElectionsCRUD():

    def create(self, number_of_seats: int):
        """
        Create election with the number of seats to be distributed
        """

        db = db_session.get()
        db_election = ElectionsModel( seats = number_of_seats )
        db.add(db_election)
        db.commit()
        db.refresh(db_election)

        return db_election

    #TODO hace metodo privado?
    def get_election(self, election_id: int):
        db = db_session.get()
        return db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()

    def get_number_of_seats(self, election_id: int):
        """
        Get the number of seats
        """
        
        db_election = self.get_election(election_id)
        if not db_election:
            raise NotFoundOnDBException

        return db_election.seats

    def update(self, election_id: int, seats: int):
        """
        Update the number of seats to be distributed
        """

        db_election = self.get_election(election_id)
        if not db_election:
            raise NotFoundOnDBException
       
        db_election.seats = seats
        db.add(db_election)
        db.commit()
        db.refresh(db_election)

        return db_election

#    def delete(self, isbn: str):
#        db = db_session.get()
#        db_book = self.get_by_isbn(isbn)
#        if not db_book:
#            raise NotFoundOnDBException
#        db.delete(db_book)
#        db.commit()
#        return db_book

elections_crud = ElectionsCRUD()

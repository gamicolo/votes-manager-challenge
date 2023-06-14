from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.elections import Elections as ElectionsModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

from app.services.votes import get_all_votes_from_db

class ElectionsCRUD():

    def create(self, number_of_seats: int, seats_distribution={}):
        """
        Create election with the number of seats to be distributed
        """

        db = db_session.get()
        db_election = ElectionsModel( seats = number_of_seats, seats_distribution = seats_distribution )
        db.add(db_election)
        db.commit()
        db.refresh(db_election)

        return db_election

    #def _get_election(self, election_id: int):
    def _get_election(self, election_id: int, db: Session):
        """
        Get election row with specific id from DB
        """
        #db = db_session.get()
        return db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()

    def get_number_of_seats(self, election_id: int):
        """
        Get the number of seats
        """
        
        #db_election = self._get_election(election_id)
        db = db_session.get()
        db_election = self._get_election(election_id, db)
        if not db_election:
            raise NotFoundOnDBException

        return db_election.seats

    def get_elections_result(self, election_id: int):
        """
        Get the seats distribution for a specific elections
        """

        #db_election = self._get_election(election_id)
        db = db_session.get()
        db_election = self._get_election(election_id, db)
        if not db_election:
            raise NotFoundOnDBException

        if db_election.seats_distribution:
            return db_election.seats_distribution

        n_seats = db_election.seats
        votes = get_all_votes_from_db(election_id)
        
        seats_distribution = self._dhont(n_seats, votes)
            
        return seats_distribution

    def _dhont(self, n_seats, votes):
        """
        n_seats is the number of seats
        votes is a dictionary with the key:value {'party':votes}
        """
        t_votes=votes.copy()
        seats={}
        for key in votes: seats[key]=0
        while sum(seats.values()) < n_seats:
            max_v= max(t_votes.values())
            next_seat=list(t_votes.keys())[list(t_votes.values()).index(max_v)]
            if next_seat in seats:
                seats[next_seat]+=1
            else:
                seats[next_seat]=1
            
            t_votes[next_seat]=votes[next_seat]/(seats[next_seat]+1)
        return seats

    def update_seats(self, election_id: int, seats: int):
        """
        Update the number of seats to be distributed
        """

        #db_election = self._get_election(election_id)
        db = db_session.get()
        db_election = self._get_election(election_id, db)
        if not db_election:
            raise NotFoundOnDBException
       
        db_election.seats = seats
        db.add(db_election)
        db.commit()
        db.refresh(db_election)

        return db_election

    def update_seats_distribution(self, election_id: int, seats_distribution: dict):
        """
        Store/Update the seats distribution
        """

        db = db_session.get()
        db_election = self._get_election(election_id, db)

        #db_election = db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()
        #db_election = self._get_election(election_id)
        if not db_election:
            raise NotFoundOnDBException
       
        db_election.seats_distribution = seats_distribution
        db.add(db_election)
        db.commit()
        db.refresh(db_election)

        return db_election

#TODO delete method
#    def delete(self, election_id: int):

elections_crud = ElectionsCRUD()

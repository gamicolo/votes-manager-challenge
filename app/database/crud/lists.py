from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.elections import Elections as ElectionsModel
from app.database.models.lists import Lists as ListsModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class ListsCRUD():

    def create(self, election_id: int, list_name: str):
        """
        Create election list
        """

        db = db_session.get()
        if not (db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()):
            raise NotFoundOnDBException
        db_list = ListsModel( election_id=election_id, name=list_name )
        db.add(db_list)
        db.commit()
        db.refresh(db_list)

        return db_list

    def get_all_lists(self, election_id: int):
        """
        Get all lists from the election
        """

        db = db_session.get()
        db_lists = db.query(ListsModel).filter(ListsModel.election_id == election_id).all() 
        if not db_lists:
            raise NotFoundOnDBException
        return db_lists.name

    def update(self, election_id: int, list_name: str):
        """
        Update the name of specific list of the election
        """

        db = db_session.get()
        if not (db.query(ElectionsModel).filter(ElectionsModel.id == election_id).first()):
            raise NotFoundOnDBException

        db_list = ListsModel( election_id=election_id, name=list_name )
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
       
        return db_list

#    def get_list_id(self, list_name: str):
#        """
#        Get election list name
#        """
#
#        db = db_session.get()
#        db_list = db.query(ListsModel).filter(ListsModel.id == list_name).first()
#        if not db_list:
#            raise NotFoundOnDBException
#        return db_list.name

lists_crud = ListsCRUD()

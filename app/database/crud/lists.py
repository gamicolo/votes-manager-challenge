from sqlalchemy.orm import Session, load_only
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
        db_rows = db.query(ListsModel).filter(ListsModel.election_id == election_id).options(load_only('name')).all()
        if not db_rows:
            raise NotFoundOnDBException

        return [row.name for row in db_rows]

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

lists_crud = ListsCRUD()

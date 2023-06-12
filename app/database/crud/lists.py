from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.lists import Lists as ListsModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class ListsCRUD():

    def create(self, list_name: str):
        """
        Create election list
        """

        db = db_session.get()
        db_list = ListsModel( name = list_name )
        db.add(db_list)
        db.commit()
        db.refresh(db_list)

        return db_list

    def get(self, list_name: str):
        """
        Get election list name
        """

        db = db_session.get()
        db_list = db.query(ListsModel).filter(ListsModel.id == list_name).first()
        if not db_list:
            raise NotFoundOnDBException
        return db_list.name

lists_crud = ListsCRUD()

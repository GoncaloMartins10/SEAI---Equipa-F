from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Date


class MixinsTables:
    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()


    def get(self, session):
        pks = [c.name for c in self.__table__.primary_key.columns]
        attr = tuple(getattr(self, pk) for pk in pks)
        try:
            aux = session.query(self.__class__).get(attr)
            self.__dict__.update(aux.__dict__)
        except Exception as e:
            session.rollback()
            raise e

    def add(self, session):
        session.add(self)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(e.__dict__['orig'])
            return error
        except Exception as e:
            session.rollback()
            return str(e)

    def update(self, session):
        pass

    def delete(self, session):
        """
        1. Search the object to delete
        2. Delete the object
        """
        try:
            self.get(session)
            session.delete(self)        
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def get_batch(self, session):
        """
        1. Search all objects with attributes defined in self
        2. return list of all objects
        """
        try:
            return session.query(self.__class__).filter(*[getattr(self.__class__, col.name) == getattr(self, col.name) for col in self.__table__.columns if getattr(self, col.name) != None]).all()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def add_batch(self, session, obj_list):
        session.bulk_save_objects(obj_list)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def delete_batch(self, session, obj_list):
        for obj in obj_list:
            obj.get(session)
            session.delete(obj)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

class MixinsTablesMeasurements:
    #date_stamp = Column(Date)

    def get_measurments(self, session):
        attr = getattr(self, 'id_transformer')
        try:
            return session.query(self.__class__).filter(self.__class__.id_transformer == attr)
        except Exception as e:
            session.rollback()
            raise e

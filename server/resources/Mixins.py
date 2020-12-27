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
        """
        1. search for the object using its primary_key
        2. update the parameters that are not the primary_key in the self object
        """
        pks = [c.name for c in self.__table__.primary_key.columns]
        attr = {pk: self.getattr(self, pk) for pk in pks}
        aux = self.__class__(**attr)
        try:
            aux.get(session)
            col_names = [col.name for col in self.__table__.columns]
            for col_name in col_names:
                if getattr(self, col_name) != None:
                    setattr(aux, col_name, getattr(self, col_name))
            session.commit()
        except Exception as e:
            raise e


    def delete(self, session):
        pass

    def get_batch(self, session):
        pass

    def add_batch(self, session):
        pass


class MixinsTablesMeasurements:
    #date_stamp = Column(Date)

    def get_measurments(self, session):
        attr = getattr(self, 'id_transformer')
        try:
            return session.query(self.__class__).filter(self.__class__.id_transformer == attr)
        except Exception as e:
            session.rollback()
            raise e


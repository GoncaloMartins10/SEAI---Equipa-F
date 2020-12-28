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
        pass

    def get_batch(self, session):
        pass

    def add_batch(self, session):
        pass


class MixinsTablesMeasurements:
    
    datestamp = Column(Date)

    def get_measurements(self, session):
        attr = getattr(self, 'id_transformer')
        try:
            return session.query(self.__class__).filter(self.__class__.id_transformer == attr)
        except Exception as e:
            session.rollback()
            raise e
    
    # Procurar nomes das classes de medição pelo subclasses do MixinsTablesMeasurements
    # 
    # def get_all_measurements(self, session):
    #     subclasses=MixinsTablesMeasurements.__subclasses__()
    #     res={}
    #     for subcls in subclasses:
    #         res[subcls]=self.subcls

    #     return res
    
    #generalizar para um class method
    #intervalo para qualquer tipo de medição
    def get_by_interval(self, session, **kwargs):
        
        attr = getattr(self, 'id_transformer')
        res = session.query(self.__class__).filter(self.__class__.id_transformer == attr)
        
        for key, value in kwargs.items():
            if key == 'mindate':
                res=res.filter(self.__class__.datestamp>=value)
            elif key == 'maxdate':
                res=res.filter(self.__class__.datestamp<=value)
        
        return res

    


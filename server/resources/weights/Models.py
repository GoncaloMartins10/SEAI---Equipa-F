from sqlalchemy import Column, Integer, Float, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from resources import Base, Session
from resources.Exceptions import AttributeException


class Weights(Base):
    __tablename__="weights"
    __table_args__ ={"schema": "ges_ativos"}

    id_weights = Column(Integer, primary_key=True)
    
    h2   = Column(Float)
    ch4  = Column(Float)
    c2h6 = Column(Float)
    c2h4 = Column(Float)
    c2h2 = Column(Float)
    co   = Column(Float)
    coh2 = Column(Float)

    dga = Column(ARRAY(Float, dimensions=2))
    oil = Column(ARRAY(Float, dimensions=2))
    
    ds = Column(Float)
    it = Column(Float)
    an = Column(Float)
    wc = Column(Float)
    c  = Column(Float)
    df = Column(Float)

    dgatc_scores  = Column(ARRAY(Float, dimensions=2))
    dgatc_quant = Column(Float)

    factor            = Column(ARRAY(Float, dimensions=1))
    micro_water       = Column(Float)
    acid_value        = Column(Float)
    dielectric_loss   = Column(Float)
    breakdown_voltage = Column(Float)

    algorithm1 = Column(ARRAY(Float, dimensions=1))
    algorithm4 = Column(ARRAY(Float, dimensions=1))

    # É assim??? --------------------------------------
    # como é que se cria a relação entre a linha de pesos e o algoritmo?
    transformer_algorithm = relationship('Transformer_Algorithm_Weights', back_populates="weights")

    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            elif key == 'id_algorithm':
                pass
            else:
                raise AttributeException()
    
    def add(self,session):
        try:
            session.add(self)
            session.commit()
        #except AttributeException as att:
        #    pass
        except SQLAlchemyError as e:
            session.rollback()
            error = str(e.__dict__['orig'])
            return error

    def get(self, session, **kwargs): #pesquisar pelo num do algoritmo
        
        query = session.query(Weights)
        
        col_names = [col.name for col in Weights.__table__.columns]
        for key, value in kwargs.items():
                if key in col_names:
                    query = query.filter(getattr(self.__class__,key)==value)
                else:
                    raise AttributeException()
        
        query = query.one()
        for col in col_names:
            setattr(self,col,getattr(query,col))


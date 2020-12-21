from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from resources import Base

from resources.Exceptions import AttributeException


class Transformer(Base):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Integer, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    algorithm_weights = relationship('Transformer_Algorithm_Weights', back_populates="transformer")

    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()

    @classmethod
    def add_batch(cls, transformer_list, session):
        session.bulk_save_objects(transformer_list) 
        try:
            session.commit()
        except Exception as e:
            raise e 

    def get(self, session):
        try:
            return session.query(Transformer).get(self.id_transformer)
        except Exception as e:
            raise e

    def add(self, session):
        session.add(self)
        try:
            session.commit()
        except Exception as e:
            raise e

    def get(self, session):
        try:
            return session.query(Transformer).get(self.id_transformer)
        except Exception as e:
            raise e




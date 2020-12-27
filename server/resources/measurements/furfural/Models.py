from resources import Base
from resources.Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

class Furfural(Base,MixinsTables,MixinsTablesMeasurements):
    __tablename__   = "furfural_measurements"
    __table_args__  = {"schema": "ges_ativos"}

    id_furfural_measurement      = Column(Integer, primary_key=True)
    id_transformer               = Column(Integer, ForeignKey('ges_ativos.transformer.id_transformer'))
    
    quantity      = Column(Float)
    timestamp_furfural_measurement    = Column(Date)

    # Aqui, furfural vai ser a respetica relação na classe Transformer
    transformer= relationship("Transformer", back_populates="furfural")
    
    # def __init__(self, **kwargs):
    #     col_names = [col.name for col in self.__table__.columns]
    #     for key, value in kwargs.items():
    #         if key in col_names:
    #             print(key,value)
    #             setattr(self, key, value)
    #         else:
    #             raise AttributeException()
    
    # @classmethod
    # def add_batch(cls, furfural_list, session):
    #     session.bulk_save_objects(furfural_list) 
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         raise e 

    # def get(self, session):
    #     try:
    #         return session.query(Furfural).get(self.id_furfural)
    #     except Exception as e:
    #         raise e

    # def add(self, session):
    #     session.add(self)
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         raise e

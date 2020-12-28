from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship

from resources import Base

from resources.Exceptions import AttributeException

from resources.Mixins import MixinsTables,MixinsTablesMeasurements


class Transformer(Base, MixinsTables):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Text, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    #algorithm_weights = relationship('Transformer_Algorithm_Weights', back_populates="transformer")
    weights = relationship('Weights', back_populates='transformer')
    furfural = relationship("Furfural", back_populates="transformer")
    load = relationship("Load", back_populates="transformer")
    oil_quality = relationship("Oil_Quality", back_populates="transformer")
    dissolved_gases = relationship("Dissolved_Gases", back_populates="transformer")

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

    def get_all_measurements(self, session):
        subclasses=MixinsTablesMeasurements.__subclasses__()
        res={}
        for subcls in subclasses:
            res[subcls]=self.subcls

        return res
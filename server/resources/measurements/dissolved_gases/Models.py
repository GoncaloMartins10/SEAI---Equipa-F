from resources import Base
from resources.Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship

class Dissolved_Gases(Base):
    __tablename__="dissolved_gas_measurements"
    __table_args__ ={"schema": "ges_ativos"}

    id_dissolved_gas_measurement = Column(Integer, primary_key=True)
    id_transformer  = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    h2 = Column(Float)
    ch4 = Column(Float)
    c2h6 = Column(Float)
    c2h4 = Column(Float)
    c2h2 = Column(Float)
    co = Column(Float)
    cOh2 = Column(Float)
    #timestamp_dissolved_gases_measurements = Column(Date)

    transformer = relationship("Transformer", back_populates="dissolved_gases")


    # @classmethod
    # def add_batch(cls, furfural_list, session):
    #     session.bulk_save_objects(furfural_list) 
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         raise e 

    
from resources import Base
from resources.Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship

class Load(Base):
    __tablename__="load_measurements"
    __table_args__ ={"schema": "ges_ativos"}

    id_load_measurement = Column(Integer, primary_key=True)
    id_transformer  = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    power_factor = Column(Float)
    load_factor = Column(Float)
    #timestamp_load_measurement = Column(Date)

    transformer = relationship("Transformer", back_populates="load")

    
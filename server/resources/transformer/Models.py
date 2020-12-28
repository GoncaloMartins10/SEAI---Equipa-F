from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship

from resources import Base

from resources.Exceptions import AttributeException

from resources.Mixins import MixinsTables


class Transformer(Base, MixinsTables):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Text, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    weights = relationship('Weights', back_populates='transformer')
    furfural = relationship("Furfural", back_populates="transformer")
    load = relationship("Load", back_populates="transformer")
    oil_quality = relationship("Oil_Quality", back_populates="transformer")
    dissolved_gases = relationship("Dissolved_Gases", back_populates="transformer")

    def __init__(self, **kwargs):
        MixinsTables.__init__(self, **kwargs)



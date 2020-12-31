from ... import Base
from ...Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship

class Maintenance(Base, MixinsTables, MixinsTablesMeasurements):
    __tablename__="maintenance"
    __table_args__ ={"schema": "ges_ativos"}

    id_maintenance = Column(Integer, primary_key=True)
    id_transformer  = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    impact_index = Column(Integer)

    transformer = relationship("Transformer", back_populates="maintenance")

    def __init__(self, **kwargs):
       MixinsTables.__init__(self, **kwargs)

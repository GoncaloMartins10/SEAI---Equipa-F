from ... import Base
from ...Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship

class Overall_Condition(Base, MixinsTables, MixinsTablesMeasurements):
    __tablename__="overall_condition"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'), primary_key=True)
    datestamp = Column(Date, primary_key=True)
    score = Column(Integer)
    transformer = relationship("Transformer", back_populates="overall_condition")

    def __init__(self, **kwargs):
       MixinsTables.__init__(self, **kwargs)

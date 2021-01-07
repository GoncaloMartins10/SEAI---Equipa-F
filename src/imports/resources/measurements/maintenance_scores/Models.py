from ... import Base
from ...Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship

class Maintenance_Scores(Base, MixinsTables, MixinsTablesMeasurements):
    __tablename__="maintenance_scores"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'), primary_key=True)
    datestamp = Column(Date, primary_key=True)
    bushings = Column(Integer)
    infra_red = Column(Integer)
    cooling = Column(Integer)
    main_tank = Column(Integer)
    oil_tank = Column(Integer)
    foundation = Column(Integer)
    grounding = Column(Integer)
    gaskets = Column(Integer)
    connectors = Column(Integer)
    oil_leaks = Column(Integer)
    oil_level = Column(Integer)
    transformer = relationship("Transformer", back_populates="maintenance_scores")

    def __init__(self, **kwargs):
       MixinsTables.__init__(self, **kwargs)

from sqlalchemy import Column, Integer, Float, ARRAY, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from resources import Base, Session
from resources.Exceptions import AttributeException
from resources.Mixins import MixinsTables


class Weights(Base,MixinsTables):
    __tablename__="weights"
    __table_args__ ={"schema": "ges_ativos"}

    id_weights = Column(Integer, primary_key=True)
    id_algorithm = Column(Integer)
    id_transformer = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    transformer = relationship("Transformer", back_populates="weights")
    
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
    

    def __init__(self, **kwargs):
        MixinsTables.__init__(self, **kwargs)

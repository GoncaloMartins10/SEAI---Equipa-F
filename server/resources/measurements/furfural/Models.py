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

    transformer= relationship("Transformer", back_populates="furfural")
    
    def __init__(self, **kwargs):
        MixinsTables.__init__(self, **kwargs)

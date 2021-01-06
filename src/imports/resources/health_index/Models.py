from sqlalchemy import Column, Integer, Float, ARRAY, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from .. import Base
from ..Exceptions import AttributeException
from ..Mixins import MixinsTables,MixinsTablesMeasurements


class Health_Index(Base,MixinsTables,MixinsTablesMeasurements):
    __tablename__="health_index"
    __table_args__ ={"schema": "ges_ativos"}

    id_health_index = Column(Integer, primary_key=True)
    id_transformer = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    id_algorithm = Column(Integer)
    
    transformer = relationship("Transformer", back_populates="health_index")

    hi = Column(Float)

    def __init__(self, **kwargs):
        MixinsTables.__init__(self, **kwargs)

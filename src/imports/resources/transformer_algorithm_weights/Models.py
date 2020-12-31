from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from resources import Base

from resources.Exceptions import AttributeException


# class Transformer_Algorithm_Weights(Base):
#     __tablename__ ="transformer_algorithm_weights"
#     __table_args__={"schema": "ges_ativos"}

#     id_transformer  = Column(Integer, ForeignKey('ges_ativos.transformer.id_transformer'), primary_key=True)
#     id_algorithm    = Column(Integer, primary_key=True)
#     id_weights      = Column(Integer, ForeignKey('ges_ativos.weights.id_weights'), primary_key=True)

#     transformer = relationship("Transformer", back_populates="algorithm_weights")
#     weights = relationship("Weights", back_populates="transformer_algorithm")

#     def __init__(self, **kwargs):
#         col_names = [col.name for col in self.__table__.columns]
#         for key, value in kwargs.items():
#             if key in col_names:
#                 print(key,value)
#                 setattr(self, key, value)
#             else:
#                 raise AttributeException()
        


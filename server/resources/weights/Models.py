from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from resources import Base

from resources.Exceptions import AttributeException


class Weights(Base):
    __tablename__="weights"
    __table_args__ ={"schema": "ges_ativos"}

    id_weights = Column(Integer, primary_key=True)
    
    H2   = Column(Float)
    CH4  = Column(Float)
    C2H6 = Column(Float)
    C2H4 = Column(Float)
    C2H2 = Column(Float)
    CO   = Column(Float)
    COH2 = Column(Float)

    DGAScores = Column(ARRAY(Float, dimensions=2))
    OilScores = Column(ARRAY(Float, dimensions=2))
    
    
    DS_Weight = Column(Float)
    IT_Weight = Column(Float)
    AN_Weight = Column(Float)
    WC_Weight = Column(Float)
    C_Weight  = Column(Float)
    DF_Weight = Column(Float)

    DGATCScores   = Column(ARRAY(Float, dimensions=2))
    DGATCQuantity = Column(Float)

    Factor                   = Column(ARRAY(Float, dimensions=1))
    Micro_Water_Weight       = Column(Float)
    Acid_Value_Weight        = Column(Float)
    Dielectric_Loss_Weight   = Column(Float)
    Breakdown_Voltage_Weight = Column(Float)

    algoritmo1 = Column(ARRAY(Float, dimensions=1))
    algoritmo4 = Column(ARRAY(Float, dimensions=1))  

    # transformer_algorithm = relationship("Transformer_Algorithm_Weights", back_populates="transformer_algorithm_weights")

    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()

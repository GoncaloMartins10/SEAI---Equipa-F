from resources import Base
from resources.Mixins import MixinsTables,MixinsTablesMeasurements
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship

class Oil_Quality(Base):
    __tablename__="oil_quality_measurements"
    __table_args__ ={"schema": "ges_ativos"}

    id_oil_quality_measurement = Column(Integer, primary_key=True)
    id_transformer = Column(Text, ForeignKey('ges_ativos.transformer.id_transformer'))
    breakdown_voltage = Column(Float)
    water_content = Column(Float)
    acidity = Column(Float)
    color = Column(Float)
    interfacial_tension = Column(Float)
    #timestamp_oil_quality_measurement = Column(Date)

    transformer = relationship("Transformer", back_populates="oil_quality")

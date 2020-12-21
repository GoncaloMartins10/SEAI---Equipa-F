
class Transformer_Algorithm_Weights(Base):
    __tablename__   = "association"
    __table_args__  = {"schema": "ges_ativos"}

    id_transformer  = Column(Integer, ForeignKey('transformer.id'), primary_key=True)
    id_weights      = Column(Integer, ForeignKey('weights.id'), primary_key=True)

    transformer     = relationship("Transformer", back_populates="transformer")
    weights         = relationship("Weights", back_populates="weights")

    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()


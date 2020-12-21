class Furfural(Base):
    __tablename__   = "furfural"
    __table_args__  = {"schema": "ges_ativos"}

    id = Column(Integer, primary_key=True)
    id_transformer  = Column(Integer, ForeignKey('transformer.id'))
    
    quatity         = Column(Float)

    # Aqui, furfural vai ser a respetica relação na classe Transformer
    transformer     = relationship("Transformer", back_populates="furfural")
    
    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()

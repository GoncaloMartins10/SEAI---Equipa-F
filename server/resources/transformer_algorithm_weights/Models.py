
class Transformer_Algorithm_Weights(Base):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Integer, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    def __init__(self, *args):
        for i in range(3):
            self.(id_transformer, )
            


from sqlalchemy import MetaData, exc, create_engine, Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



db_url = {'drivername': 'postgres',
          'username': 'postgres',
          'password': 'postgres',
          'host': 'localhost',
          'port': 5432,
          'database':'seai'}

engine = create_engine(URL(**db_url), echo=True)
try:
    engine.connect()
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
except (Exception, exc.SQLAlchemyError) as error:
    print("\t<<< Error connecting to DataBase >>>\n", error)


class AttributeException(Exception):
    def __init__(self, message=None):
        self.message = self.message if message!=None else self.__class__.__name__
        super.__init__(self.message)

class Transformer_Algorithm_Weights(Base):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Integer, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    def __init__(self, *args):
        for i in range(3):
            self.(id_transformer, )
            

class Transformer(Base):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Integer, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    algorithm_weights = relationship("Transformer_Algorithm_Weights", back_populates="transformer_algorithm_weights")

    def __init__(self, **kwargs):
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()
            


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

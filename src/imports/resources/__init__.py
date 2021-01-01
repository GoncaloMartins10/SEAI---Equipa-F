from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

with open("src/imports/resources/config.json", "r") as config: 
    configuations = json.load(config)

selected = configuations["Selected_DB"]
db_url = configuations[selected]

engine = create_engine(URL(**db_url), echo=False)
try:
    engine.connect()
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
except Exception as e:
    print("\t<<< Error connecting to DataBase >>>\n", e)

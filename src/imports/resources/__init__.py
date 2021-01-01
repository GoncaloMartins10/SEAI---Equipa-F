from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os

cwd = os.getcwd()
repo_name = 'SEAI---Equipa-F'
repo_dir = cwd[:cwd.rindex(repo_name) + len(repo_name)] # retira tudo depois de 'SEAI---Equipa-F'
config_path = os.path.join(repo_dir,"src/imports/resources/config.json")

with open(config_path, "r") as config: 
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

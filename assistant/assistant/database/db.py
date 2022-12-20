from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base


file_config = Path(__file__).parent.parent.parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

# user = config.get("DB-DEV", "user")
# password = config.get("DB-DEV", "password")
# host = config.get("DB-DEV", "domain")
# port = config.get("DB-DEV", "port")
db_name = config.get("DB-DEV", "db_name")

# url = f'sqlite://{user}:{password}@{host}:{port}/{db_name}'

path = Path('~').expanduser()
# db_name = 'assistant.db'
url = f'sqlite:///{path / db_name}'

Base = declarative_base()
engine = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from configs import get_config

env_variables = get_config.get_settings()

db_uri = f"mysql+pymysql://{env_variables.db_user}:{env_variables.db_pass}@{env_variables.db_host}:{env_variables.db_port}/{env_variables.db_name}"

db_engine = create_engine(url=db_uri, pool_pre_ping=True)

Base = declarative_base()

session = sessionmaker(bind=db_engine)


def get_db():
    try:
        db = session()
        yield db
    except Exception as err:
        print("Unable to Get a DB Connection")
    finally:
        db.close()

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from configs import get_config
from helpers import response_parser

logger = logging.getLogger(__name__)

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
        logger.error("Error occurred in get_db: %s", err, exc_info=True)
        raise response_parser.generate_response(
            code=500, message="Error Occurred in Connection", success=False
        )
    finally:
        db.close()

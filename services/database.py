import logging
from sqlalchemy.orm import Session

from models import user
from helpers import response_parser

logger = logging.getLogger(__name__)


def get_user_by_id(db: Session, user_id: int):
    try:
        return (
            db.query(user.User)
            .filter(user.User.id == user_id)
            .filter(user.User.is_active == 1)
            .first()
        )
    except Exception as err:
        logger.error("Error occured in get_user_by_id %s", err, exc_info=True)
        raise response_parser.generate_response(
            code=500, message="Error occurred", success=False
        )

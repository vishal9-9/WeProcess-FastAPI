import logging
from fastapi import Depends, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from configs.get_config import get_settings
from database.engine import get_db
from services import database
from helpers import response_parser


logger = logging.getLogger(__name__)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


class TokenGenerator:
    @staticmethod
    def encode_token(id: str, expire_time_in_mins: int, data: dict = None):
        """
        The encode_token function takes in a user object and returns a token

        :param user: The user id that we want to encode
        :return: A token
        """
        logger.info("encode_token function is exceuting")
        try:
            settings = get_settings()
            payload = {
                "exp": datetime.now(timezone.utc)
                + timedelta(minutes=expire_time_in_mins),
                "sub": f"{id}",
                "data": data,
            }

            token = jwt.encode(
                payload, settings.secret_jwt_key, algorithm=settings.algorithm
            )
            return token
        except Exception as err:
            logger.error("Error occurred in Token Generation %s", err, exc_info=True)
            raise response_parser.generate_response(
                code=500, message="Unable to encode data", success=False
            )

    @staticmethod
    def decode_token(token: str, db: Session):
        """
        It takes a token, decodes it, and returns the decoded token

        :param db: db session
        :param token: The token to decode
        :return: A dictionary with the user's id.
        """
        try:
            settings = get_settings()
            credentials_exception = response_parser.generate_response(
                code=401, message="Could not validate credentials", success=False
            )
            payload = jwt.decode(
                token, settings.secret_jwt_key, algorithms=[settings.algorithm]
            )
            user_id = int(payload.get("sub"))
            if user_id is None:
                raise credentials_exception
        except JWTError as err:
            logger.error("Error occurred in token decoding %s", err, exc_info=True)
            raise credentials_exception
        user = database.get_user_by_id(db=db, user_id=user_id)
        if user is None:
            raise credentials_exception
        if not user.is_active == 1:
            raise response_parser.generate_response(
                code=401, message="User is blocked", success=False
            )
        return user

    @staticmethod
    def get_current_user(
        token: str = Depends(oauth_scheme), db: Session = Depends(get_db)
    ):
        return TokenGenerator.decode_token(token=token, db=db)

    @staticmethod
    def decode_invite_token(token: str):
        try:
            settings = get_settings()
            payload = jwt.decode(
                token, settings.secret_jwt_key, algorithms=[settings.algorithm]
            )
            added_by = int(payload.get("sub"))
            if added_by is None:
                raise response_parser.generate_response(
                    message="Invalid token",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False,
                )
        except JWTError as err:
            logger.error("Error occurred in token decoding %s", err, exc_info=True)
            raise response_parser.generate_response(
                message="Invalid token", code=status.HTTP_400_BAD_REQUEST, success=False
            )
        if (
            payload.get("data") is not None
            and payload.get("data").get("type") == "Invite"
        ):
            return payload
        raise response_parser.generate_response(
            message="Invalid token", code=status.HTTP_400_BAD_REQUEST, success=False
        )

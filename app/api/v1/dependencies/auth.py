from fastapi import HTTPException, status, Depends, Request
from db.models.user import User
from db.models.admin import Admin
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.config import settings
from core.security import verify_password
import logging
from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta, UTC

logger = logging.getLogger(__name__)


oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authenticate_user(email, password):
    logger.info(f"Authenticating user: {email}")
    user = None
    user_type = None
    try:
        user = await Admin.get(email = email)
        if user:
            user_type = "admin"
            logger.info(f"Admin user found: {email}")

    except DoesNotExist:
        logger.info(f"No admin user found with email: {email}")


    if not user:
        try:
            user = await User.get(email = email)
            if user:
                user_type = "user"
                logger.info(f"User found: {email}")
        except DoesNotExist:
            logger.info(f"No user found with email: {email}")

    if user and await verify_password(password, user.hashed_password):
        logger.info(f"User authenticated: {email}")
        return user, user_type
        
    logger.warning(f"Authentication failed for user: {email}")
    return None, None


async def token_generator(email: str, password: str):
    user, user_type = await authenticate_user(email, password)

    if not user:
        raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
            )
        )
    
    expiry_delta = datetime.now(UTC) + timedelta(hours=36)
    token_data = {
        "id": user.id,
        "email": user.email,
        "user_type": user_type,
        "exp":str(expiry_delta)
    }

    token = jwt.encode(token_data, settings.SECRET_KEY, algorithm = settings.ALGORITM)
    logger.info(f"Token generated for user: {email}")
    return token


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITM])
        email: str = payload.get("email")
        user_id: str = payload.get("id")
        user_type: str = payload.get("user_type")
        if email is None or user_id is None or user_type is None:
            raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
                )
            )
    
    except:
        raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
            )
        )
    
    user = None
    if user_type == "admin":
        user = await Admin.get(email = email)
    if user_type == "user":
        user = await User.get(email = email)

    if user is None:
        raise(
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user credentials",
                headers={"WWW-Authenicate": "Bearer"}
            )
        )
    
    return user
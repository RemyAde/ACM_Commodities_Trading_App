from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
from db.models.user import User
from core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITM])
        user = await User.get(id = payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
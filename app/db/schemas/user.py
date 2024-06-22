from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.user import User
from pydantic import BaseModel, EmailStr


User_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "role"))
User_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("hashed_password", "is_verified", "date_created", "profile_image"))


class User_pydanticIn(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    password: str

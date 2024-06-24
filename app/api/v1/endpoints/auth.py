from datetime import datetime, UTC
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status, Depends, Response
from starlette.responses import RedirectResponse

from db.schemas.admin import admin_pydantic, admin_pydanticIn
from db.models.admin import Admin
from pydantic import BaseModel, EmailStr

# Authentication
from core.security import get_hashed_password
from api.v1.dependencies.auth import token_generator

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["/auth"]
)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def login_user(form: LoginRequest, response: Response):
    token = await token_generator(form.email, form.password)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, domain="https://acm-c.vercel.app")
    return {
        "status": "ok",
        "msg": "login successful"
    }


@router.post("/admin/registration", status_code=201)
async def admin_registration(user: admin_pydanticIn): # type: ignore
    user_info = user.dict(exclude_unset=True)
    user_info["hashed_password"] = get_hashed_password(user_info["hashed_password"])
    user_obj = await Admin.create(**user_info)

    return {
        "status":"success",
        "detail":"registration successful"
    }


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return{"msg": "logout successful"}
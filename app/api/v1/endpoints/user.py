from fastapi import APIRouter, Depends, status, HTTPException
from db.schemas.user import User_pydantic, User_pydanticIn, User_pydanticOut
from pydantic import BaseModel
from db.models.user import User
from core.security import get_hashed_password
from api.v1.dependencies.auth import get_current_user
from core.security import verify_password, get_hashed_password

router = APIRouter(
    prefix="/user",
    tags=["/user"]
)


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str


class UserPasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


@router.post("/register-user", status_code=status.HTTP_201_CREATED)
async def user_registration(user_info: User_pydanticIn): # type: ignore 
    
    user_obj = await User.create(
        email = user_info.email,
        first_name = user_info.first_name,
        last_name = user_info.last_name,
        phone_number = user_info.phone_number,
        hashed_password = get_hashed_password(user_info.password)
    )

    await user_obj.save()

    return {
        "status": "created",
        "msg": "registration successful"
    }


@router.get("/user-details", status_code=status.HTTP_200_OK)
async def get_user_details(user: User_pydantic = Depends(get_current_user)): # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not authenticated to perform this action"
        )
    
    user_obj = await User_pydanticOut.from_tortoise_orm(user)
    
    return {
        "msg": "success",
        "data": user_obj
    }


@router.put("/edit-user-info", status_code=200)
async def edit_user_info(user_request: UserUpdateRequest, user: User_pydantic = Depends(get_current_user)): # type: ignore
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    user.first_name = user_request.first_name
    user.last_name = user_request.last_name
    user.phone_number = user_request.phone_number
    await user.save()
    user_obj = await User_pydanticOut.from_tortoise_orm(user)

    return {
        "msg": "success",
        "data": user_obj
    }


@router.put("/change-password", status_code=200)
async def change_user_password(user_request: UserPasswordRequest, user: User_pydantic = Depends(get_current_user)): # type: ignore
    if user is None:
        raise HTTPException (status_code=401, detail="Authentication failed")
    
    if not await verify_password(user_request.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is not correct")
    
    if user_request.new_password != user_request.confirm_password:
        return HTTPException(status_code=400, detail="Confirm password failed")
    
    if user_request.new_password == user_request.confirm_password:
        user.hashed_password = get_hashed_password(user_request.new_password)

    await user.save()

    return{"msg": "Password changed!"}
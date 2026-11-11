from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.configdb import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["Users"])


# CREATE USER
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_crud.create_user(db, user_data)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


# GET ALL USERS
@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users(db)


# GET SINGLE USER
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# UPDATE USER
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        user = await user_crud.update_user(db, user_id, user_data)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


# DELETE USER
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.delete_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return None

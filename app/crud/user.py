from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


# CREATE USER
async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:

    new_user = User(**user_data.model_dump())

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


# GET ALL USERS
async def get_users(
    db: AsyncSession,
) -> list[User]:

    result = await db.execute(select(User).order_by(User.id))

    return list(result.scalars().all())


# GET SINGLE USER
async def get_user(
    db: AsyncSession,
    user_id: int,
) -> User | None:

    result = await db.execute(select(User).where(User.id == user_id))

    return result.scalar_one_or_none()


# UPDATE USER
async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate,
) -> User | None:

    user = await get_user(db, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


# DELETE USER
async def delete_user(
    db: AsyncSession,
    user_id: int,
) -> User | None:

    user = await get_user(db, user_id)

    if user is None:
        return None

    await db.delete(user)
    await db.commit()

    return user

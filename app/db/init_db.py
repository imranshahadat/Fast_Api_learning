from app.db.configdb import engine, Base

# Import models so SQLAlchemy registers them.
from app.models.user import User


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

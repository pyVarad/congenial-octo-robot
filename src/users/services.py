from sqlmodel import select
from .models import User
from src.utils.utils import get_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import datetime


class UserService:
    async def get_all_users(self, session: AsyncSession) -> List[User]:
        """
        Get all users.
        """
        statement = select(User)
        result = await session.exec(statement)
        users = result.all()
        return users

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> User:
        """
        Get a user by ID.
        """
        statement = select(User).where(User.id == user_id)
        user = await session.exec(statement)
        return user.first() if user else None

    async def create_user(self, user_info, session: AsyncSession):
        """
        Create a new user.
        """
        user = User(**user_info.model_dump())
        if self.user_exists(user.email, session):
            raise ValueError("User with this email already exists")

        user.password = get_password_hash(user.password)
        user.created_at = user.updated_at = datetime.now()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update_user(self, user_id: int, user_data, session: AsyncSession) -> User:
        """
        Update a user by ID.
        """
        user = await self.get_user_by_id(user_id, session)
        if not user:
            return None
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def delete_user(self, user_id: int, session: AsyncSession) -> User:
        """
        Delete a user by ID.
        """
        user = await self.get_user_by_id(user_id, session)
        if not user:
            return None
        await session.delete(user)
        await session.commit()
        return user
    
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        """
        Get a user by email.
        """
        statement = select(User).where(User.email == email)
        user = await session.exec(statement)
        return user.first() if user else None
    
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        """
        Check if a user exists by email.
        """
        user = self.get_user_by_email(email, session)
        return user is not None
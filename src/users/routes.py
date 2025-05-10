from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .services import UserService
from src.db.main import get_session
from .schemas import CreateUser
from .models import User
from typing import List


users_router = APIRouter()
service = UserService()

@users_router.get(
    path="/",
    description="Get all users",
    status_code=status.HTTP_200_OK,
    response_model=List[User],
    responses={
        status.HTTP_200_OK: {
            "description": "List of users",
        },
    },
    summary="Get all users",
)
async def get_users(session: AsyncSession = Depends(get_session)):
    """
    Get all users.
    """
    return await service.get_all_users(session)

@users_router.get(
    "/{user_id}",
    description="Get a user by ID",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
    summary="Get a user by ID",
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """
    Get a user by ID.
    """
    user = await service.get_user_by_id(user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@users_router.post(
    "/signup",
    description="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "User already exists",
        },
    },
    summary="Create a new user",
)
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    """
    Create a new user.
    """
    try:
        user = await service.create_user(user, session=session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return user

@users_router.patch(
    "/{user_id}",
    description="Update a user by ID",
    status_code=status.HTTP_200_OK,
    response_model=User,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
    summary="Update a user by ID",
)
async def update_user(user_id: int, user: CreateUser, session: AsyncSession = Depends(get_session)):
    """
    Update a user by ID.
    """
    user = await service.update_user(user_id, user, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@users_router.delete(
    "/{user_id}",
    description="Delete a user by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
    },
    summary="Delete a user by ID",
)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """
    Delete a user by ID.
    """
    user = await service.delete_user(user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


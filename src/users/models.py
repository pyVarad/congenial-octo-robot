from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(
        sa_column=Column("username", type_=pg.CHAR, unique=True, nullable=False)
    )
    first_name: str = Field(
        sa_column=Column("first_name", type_=pg.CHAR, nullable=False)
    )
    last_name: str = Field(sa_column=Column("last_name", type_=pg.CHAR, nullable=False))
    email: str = Field(
        sa_column=Column("email", unique=True, type_=pg.CHAR, nullable=False)
    )
    password: str = Field(
        sa_column=Column("password", type_=pg.CHAR, nullable=False), exclude=True
    )
    is_verified: bool = Field(
        default=False, sa_column=Column("is_verified", type_=pg.BOOLEAN, nullable=False)
    )
    created_at: str = Field(
        sa_column=Column(
            "created_at",
            type_=pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now,
        ),
    )
    updated_at: str = Field(
        sa_column=Column(
            "updated_at",
            type_=pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now,
        ),
    )

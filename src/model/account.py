from __future__ import annotations

from pydantic import BaseModel, Field

from src.model.user_avatar_id import UserAvatarId


class AccountInfo(BaseModel):
    id: str
    last_updated: str = Field(..., alias="lastUpdated")
    avatar: str
    avatar_id: UserAvatarId = Field(..., alias="avatarId")
    name: str
    level: int
    power: int
    avatar_url: str = Field(..., alias="avatarUrl")

    class Config:
        use_enum_values = True


class Accounts(BaseModel):
    __root__: list[AccountInfo]

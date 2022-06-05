from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int] = None
    phone: Optional[str] = None


class UserCreateIn(UserBase):
    pass


class UserOut(UserBase):
    id: int


class UserPatchIn(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
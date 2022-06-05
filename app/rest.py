from typing import Any
from fastapi import APIRouter, HTTPException

from . import crud
from .schemas import UserCreateIn, UserOut, UserPatchIn

router = APIRouter(prefix="/users")


class NOT_FOUND_ERROR(HTTPException):

    def __init__(self, status_code: int = 404, detail: Any = None) -> None:
        detail = detail or "Not found."
        super().__init__(status_code, detail)


@router.get("/", response_model=list[UserOut])
def list_users():
    return [UserOut(**u) for u in crud.list_users()]


@router.post("/", response_model=UserOut)
def create_user(data: UserCreateIn):
    return UserOut(**crud.create_user(data.dict()))


@router.get("/{id}", response_model=UserOut)
def retrieve_user(id: int):
    user = crud.get_user_by_id(id)
    if not user:
        raise NOT_FOUND_ERROR
    return UserOut(**user)


@router.put("/{id}", response_model=UserOut)
def update_user(id: int, data: UserCreateIn):
    user = crud.update_user(id, data.dict(exclude_unset=True))
    if not user:
        user = crud.create_user(data.dict(), id_=id)
    return UserOut(**user)


@router.patch("/{id}", response_model=UserOut)
def partialy_update_user(id: int, data: UserPatchIn):
    user = crud.update_user(id, data.dict(exclude_unset=True))
    if not user:
        raise NOT_FOUND_ERROR
    return UserOut(**user)
    

@router.delete("/{id}", status_code=204)
def deete_user(id: int):
    crud.delete_user(id)

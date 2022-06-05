from typing import Any
from fastapi import Body
import fastapi_jsonrpc as jsonrpc
from pydantic import BaseModel

from app.schemas import UserCreateIn, UserOut, UserPatchIn

from . import crud


app = jsonrpc.API()

api_v1 = jsonrpc.Entrypoint('/api/v1/jsonrpc') # type: ignore

from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str


class MyError(jsonrpc.BaseError):
    CODE = 5000
    MESSAGE = 'My error'

    class DataModel(BaseModel):
        details: str


class UserDoesNotExist(jsonrpc.BaseError):
    CODE = 6000
    MESSAGE = "User doesn't exist"


@api_v1.method()
def echo(
    data: str = Body(...),
) -> str:
    if data == 'error':
        raise MyError(data={'details': 'error'})
    else:
        return data


@api_v1.method(errors=[UserDoesNotExist])
def list_users() -> list[UserOut]:
    return [UserOut(**u) for u in crud.list_users()] 


@api_v1.method(errors=[UserDoesNotExist])
def get_user(id: int) -> UserOut:
    user = crud.get_user_by_id(id)
    if not user:
        raise UserDoesNotExist(data={"user_id": id})
    return UserOut(**user)


@api_v1.method()
def create_user(data: UserCreateIn) -> UserOut:
    return UserOut(**crud.create_user(data.dict()))



@api_v1.method()
def update_user(id: int, data: UserCreateIn) -> UserOut:
    user = crud.update_user(id, data.dict(exclude_unset=True))
    if not user:
        user = crud.create_user(data.dict(), id_=id)
    return UserOut(**user)


@api_v1.method(errors=[UserDoesNotExist])
def partialy_update_user(id: int, data: UserPatchIn) -> UserOut:
    user = crud.update_user(id, data.dict(exclude_unset=True))
    if not user:
        raise UserDoesNotExist(data={"user_id": id})
    return UserOut(**user)
    

@api_v1.method()
def delete_user(id: int):
    crud.delete_user(id)


@api_v1.method(errors=[UserDoesNotExist])
def say_hello(id: int) -> str:
    user = crud.get_user_by_id(id)
    if not user:
        raise UserDoesNotExist(data={"user_id": id})
    return f"Hello. My name is {user['first_name']} {user['last_name']}"



app.bind_entrypoint(api_v1)

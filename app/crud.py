from typing import Optional
from pydantic import BaseModel

USERS = {}

def _alloc_id(storage: dict) -> int:
    cur_id_ = max((*storage.keys(), 0))
    return cur_id_ + 1

def list_users() -> list[dict]:
    return list(USERS.values())

def create_user(data: dict, id_: Optional[int] = None) -> dict:
    if not id_:
        id_ = _alloc_id(USERS)
    USERS[id_] = {**data, "id": id_}
    return USERS[id_]

def get_user_by_id(id_: int) -> Optional[dict]:
    return USERS.get(id_)

def update_user(id_: int, data: dict) -> Optional[dict]:
    user = USERS.get(id_)
    if not user:
        return None
    USERS[id_] = {**user, **data}
    return USERS[id_]

def delete_user(id_: int) -> Optional[dict]:
    return USERS.pop(id_, None)


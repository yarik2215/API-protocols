from typing import Optional

import strawberry
from strawberry.asgi import GraphQL

from . import crud


# @strawberry.input
@strawberry.type
class User:
    id: strawberry.ID
    first_name: str
    last_name: str
    age: Optional[int]
    phone: Optional[str]


@strawberry.type
class Response:
    ok: bool
    message: Optional[str] = None


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        user = crud.get_user_by_id(int(id))
        return User(**user) if user else None

    @strawberry.field
    def users(self) -> list[User]:
        users = crud.list_users()
        return [User(**u) for u in users]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, first_name: str, last_name: str, age: Optional[int] = None, phone: Optional[str] = None) -> User:
        user = crud.create_user({"first_name": first_name, "last_name": last_name, "age": age, "phone": phone})
        return User(**user)

    @strawberry.mutation
    def update_user(self, id: strawberry.ID, age: Optional[int] = None, phone: Optional[str] = None) -> User:
        data = {}
        if age is not None:
            data["age"] = age
        if phone is not None:
            data[phone] = phone
        user = crud.update_user(int(id), data)
        if not user:
            raise Exception("Can't find user")
        return User(**user)

    @strawberry.mutation
    def delete_user(self, id: strawberry.ID) -> Response:
        user = crud.delete_user(int(id))
        message = "user deleted" if user else "user doesn't exist"
        return Response(True, message)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

from fastapi import FastAPI
from .websocket import router as ws_router
from .rest import router as rest_router
from .graphql import graphql_app

from .jsonrpc import app as jrpc_app

app = FastAPI()

@app.get("/hello", response_model=str)
def hello() -> str:
    return "Hello world"

# # websocket
# app.include_router(ws_router, tags=["Websockets"])

# # rest
# app.include_router(rest_router, tags=["Rest"])

# # graphql
# app.add_route("/graphql", graphql_app)
# app.add_websocket_route("/graphql", graphql_app)

# app.mount("/jrpc/", jrpc_app)

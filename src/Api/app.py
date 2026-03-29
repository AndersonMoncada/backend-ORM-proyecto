from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.config import create_tables

from src.Api.MicroEntidades import (
    router_acuatica,
    router_electronica,
    router_mecanica,
    router_fisica,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    import src.Entities

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(router_acuatica)
app.include_router(router_electronica)
app.include_router(router_mecanica)
app.include_router(router_fisica)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"msg": "API funcionando 🚀"}

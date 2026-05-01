from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ← Agregado
from src.database.config import create_tables

from . import (
    Usuario,
    Titular,
    Visitante,
    Accede,
    Sede,
    Atraccion,
    Entrada,
)

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


app = FastAPI(title="Parque de Diversiones API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Frontend Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(Usuario.router)
app.include_router(Titular.router)
app.include_router(Visitante.router)
app.include_router(Accede.router)
app.include_router(Sede.router)
app.include_router(Atraccion.router)
app.include_router(Entrada.router)

app.include_router(router_acuatica)
app.include_router(router_electronica)
app.include_router(router_mecanica)
app.include_router(router_fisica)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root():
    return {"msg": "API funcionando 🚀"}
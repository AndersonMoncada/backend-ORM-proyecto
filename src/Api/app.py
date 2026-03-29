from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables


from . import Usuario, Titular, Visitante

from src.Api.MicroEntidades import (
    router_acuatica,
    router_electronica,
    router_mecanica,
    router_fisica,
)



@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Registra modelos y crea tablas si no existen (misma lógica que init_db.py)
    from src.Entities import Entrada  # noqa: F401

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)


app.include_router(Usuario.router)
app.include_router(Titular.router)
app.include_router(Visitante.router)
app.include_router(router_acuatica)
app.include_router(router_electronica)
app.include_router(router_mecanica)
app.include_router(router_fisica)
app.include_router(Sede.router)
app.include_router(Atraccion.router)
app.include_router(Entrada.router)
app.include_router(Accede.router)


@app.get("/health")
def health() -> dict[str, str]:

    return {"status": "ok"}


@app.get("/")
def root():
    return {"msg": "API funcionando 🚀"}


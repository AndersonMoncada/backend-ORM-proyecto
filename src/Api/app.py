from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables

from . import Entrada


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Registra modelos y crea tablas si no existen (misma lógica que init_db.py)
    from src.Entities import Entrada  # noqa: F401

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(Entrada.router)



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
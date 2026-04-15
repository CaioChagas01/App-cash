from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calcular_cashback(tipo, valor):
    regras = {
        "comum": 0.05,
        "premium": 0.10,
        "vip": 0.15
    }
    return valor * regras.get(tipo, 0)

@app.post("/cashback")
async def calcular(request: Request, data: dict):
    db = SessionLocal()

    ip = request.client.host
    cashback = calcular_cashback(data["tipo_cliente"], data["valor"])

    registro = models.Cashback(
        ip=ip,
        tipo_cliente=data["tipo_cliente"],
        valor=data["valor"],
        cashback=cashback
    )

    db.add(registro)
    db.commit()

    return {"cashback": cashback}

@app.get("/historico")
async def historico(request: Request):
    db = SessionLocal()
    ip = request.client.host

    registros = db.query(models.Cashback).filter(models.Cashback.ip == ip).all()

    return registros
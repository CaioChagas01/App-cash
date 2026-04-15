from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models

# ⚠️ Em produção ideal seria Alembic, mas aqui funciona
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (para Vercel / frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois você pode travar isso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# REGRA DE CASHBACK
# ------------------------
def calcular_cashback(tipo, valor):
    regras = {
        "comum": 0.05,
        "premium": 0.10,
        "vip": 0.15
    }
    return valor * regras.get(tipo, 0)


# ------------------------
# ENDPOINT: CALCULAR CASHBACK
# ------------------------
@app.post("/cashback")
async def calcular_cashback_endpoint(request: Request, data: dict):
    db = SessionLocal()
    try:
        ip = request.client.host

        cashback = calcular_cashback(
            data["tipo_cliente"],
            data["valor"]
        )

        registro = models.Cashback(
            ip=ip,
            tipo_cliente=data["tipo_cliente"],
            valor=data["valor"],
            cashback=cashback
        )

        db.add(registro)
        db.commit()

        return {
            "status": "ok",
            "cashback": cashback
        }

    finally:
        db.close()


# ------------------------
# ENDPOINT: HISTÓRICO
# ------------------------
@app.get("/historico")
async def historico(request: Request):
    db = SessionLocal()
    try:
        ip = request.client.host

        registros = db.query(models.Cashback).filter(
            models.Cashback.ip == ip
        ).all()

        return [
            {
                "tipo_cliente": r.tipo_cliente,
                "valor": r.valor,
                "cashback": r.cashback
            }
            for r in registros
        ]

    finally:
        db.close()


# ------------------------
# TESTE RÁPIDO
# ------------------------
@app.get("/")
def home():
    return {
        "status": "API rodando 🚀",
        "endpoints": ["/cashback", "/historico"]
    }
from sqlalchemy import Column, Integer, Float, String
from database import Base

class Cashback(Base):
    __tablename__ = "cashbacks"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    tipo_cliente = Column(String)
    valor = Column(Float)
    cashback = Column(Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Encarregado(Base):  # ou Usuario, conforme sua tabela
    __tablename__ = "usuarios"  # nome da tabela já existente

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    senha = Column(String)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "ENCARREGADO"  # Nome da tabela no seu banco

    id = Column(Integer, primary_key=True)
    usuario = Column(String, nullable=False)
    senha = Column(String, nullable=False)
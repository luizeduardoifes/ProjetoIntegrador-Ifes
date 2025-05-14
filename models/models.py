from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Substitua o caminho abaixo com o caminho do seu banco de dados
DATABASE_URL = "sqlite:///./usuarios.db"  # ou PostgreSQL, MySQL, etc.

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Apenas para SQLite
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sqlite_file_name = "dados.db"
sqlit_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlit_url, connect_args=connect_args) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
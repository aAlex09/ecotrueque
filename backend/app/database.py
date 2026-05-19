from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL

# Crear motor de BD
engine = create_engine(DATABASE_URL, echo=True)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para inyectar la sesión en las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

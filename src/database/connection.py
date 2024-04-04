from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "postgresql://postgres:bharath@localhost/scrap"
DATABASE_URL = "postgresql://postgres:bharath@172.17.0.1:5433/scrap"
engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
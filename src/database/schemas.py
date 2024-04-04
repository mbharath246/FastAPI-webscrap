from sqlalchemy import Column, Integer, String, BigInteger
from src.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(BigInteger, nullable=False)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
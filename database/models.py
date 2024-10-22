# models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Controller(Base):
    __tablename__ = "controller"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    ip = Column(String, unique=True, index=True)
    scp_number = Column(Integer, primary_key=True, index=True)
    channel_number = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

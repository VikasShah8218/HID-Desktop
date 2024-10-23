# models.py
from sqlalchemy import Column, Integer, String ,UniqueConstraint
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
    scp_number = Column(Integer,unique=True,index=True)
    channel_number = Column(Integer,unique=True, index=True)
    name = Column(String, index=True)

class Card(Base):
    __tablename__ = "card"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_id = Column(String, index=True)
    facility_code = Column(Integer, index=True)
    issue_code = Column(Integer, index=True)
    card_holder_name = Column(String, index=True)
    card_holder_phone_no = Column(String, unique=True, index=True)
    alvl = Column(String, index=True)

    # Unique constraint on card_id and facility_code
    __table_args__ = (
        UniqueConstraint('card_id', 'facility_code', name='uq_card_facility'),
    )
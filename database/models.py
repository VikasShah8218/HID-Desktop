# models.py
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, DateTime ,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

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

    # Relationship to TransactionLog model
    transactions = relationship("TransactionLog", back_populates="card")

class Controller(Base):
    __tablename__ = "controller"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, unique=True, index=True)
    scp_number = Column(Integer, unique=True, index=True)
    channel_number = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)

    # Relationship to TransactionLog model
    transactions = relationship("TransactionLog", back_populates="controller")

class TransactionLog(Base):
    __tablename__ = "transaction_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # ForeignKey references to other tables
    card_id = Column(Integer, ForeignKey("card.id"), nullable=False)
    controller_id = Column(Integer, ForeignKey("controller.id"), nullable=False)
    
    # Relationship to fetch the complete Card and Controller object
    card = relationship("Card", back_populates="transactions")
    controller = relationship("Controller", back_populates="transactions")

    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
    log_type = Column(Integer, nullable=False)
    log_detail = Column(String, nullable=False)



class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_content = Column(Text, nullable=False)  # Store the .ini file content as text
    file_name = Column(String, nullable=False)   # Name of the file (e.g., filename.ini)
    purpose = Column(String, nullable=False)     # Purpose of the file
    notes = Column(Text, nullable=True)          # Optional notes about the file
    uploaded_on = Column(DateTime, default=datetime.utcnow, nullable=False)  # Date and time of upload

    def __repr__(self):
        return f"<UploadedFile(file_name='{self.file_name}', purpose='{self.purpose}')>"
    



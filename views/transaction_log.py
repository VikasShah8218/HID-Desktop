from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import TransactionLog, Card, Controller
from datetime import datetime
from  database.database import get_db


# Create a new transaction log entry
def create_transaction_log(db: Session, card_id: str, controller_id: int, log_type: int, log_detail: str):
    print("*" * 50, "Starting", "*" * 50)
    # Check if the card and controller exist
    card_exists = db.query(Card).filter(Card.card_id == card_id).first()
    controller_exists = db.query(Controller).filter(Controller.scp_number == controller_id).first()

    if not card_exists:
        raise ValueError(f"Card with ID {card_id} does not exist.")
    if not controller_exists:
        raise ValueError(f"Controller with ID {controller_id} does not exist.")

    # Proceed to create the transaction log if both exist
    transaction_log = TransactionLog(
        card_id=card_exists.id,  # Use the actual card primary key ID here
        controller_id=controller_exists.id,
        log_type=log_type,
        log_detail=log_detail,
        created_on=datetime.utcnow()
    )
    db.add(transaction_log)
    db.commit()
    db.refresh(transaction_log)
    return transaction_log

# Retrieve a transaction log entry by ID
def get_transaction_log(db: Session, transaction_id: int):
    return db.query(TransactionLog).filter(TransactionLog.id == transaction_id).first()

# Retrieve all transaction logs, with optional limit and offset
def get_all_transaction_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TransactionLog).offset(skip).limit(limit).all()

# Update a transaction log entry
def update_transaction_log(db: Session, transaction_id: int, log_type: int = None, log_detail: str = None):
    transaction_log = db.query(TransactionLog).filter(TransactionLog.id == transaction_id).first()
    if not transaction_log:
        return None
    
    # Update fields if new values are provided
    if log_type is not None:
        transaction_log.log_type = log_type
    if log_detail is not None:
        transaction_log.log_detail = log_detail
    transaction_log.updated_on = datetime.utcnow()  # Optional: track when it was updated

    db.commit()
    db.refresh(transaction_log)
    return transaction_log

# Delete a transaction log entry by ID
def delete_transaction_log(db: Session, transaction_id: int):
    transaction_log = db.query(TransactionLog).filter(TransactionLog.id == transaction_id).first()
    if not transaction_log:
        return None
    
    db.delete(transaction_log)
    db.commit()
    return transaction_log

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Card  

def create_card(db: Session, card_id: str, facility_code: int, issue_code: int, card_holder_name: str, card_holder_phone_no: str, alvl: str):
    new_card = Card(
        card_id=card_id,
        facility_code=facility_code,
        issue_code=issue_code,
        card_holder_name=card_holder_name,
        card_holder_phone_no=card_holder_phone_no,
        alvl=alvl
    )
    try:
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        return new_card
    except IntegrityError:
        db.rollback()
        
        raise ValueError(f"Card with combination of card_id '{card_id}' and facility_code '{facility_code}' already exists.")

def get_card_by_id(db: Session, card_id: str):
    return db.query(Card).filter(Card.card_id == card_id).first()

def get_all_cards(db: Session):
    return db.query(Card).all()

def update_card(db: Session, card_id: str, facility_code: int, **kwargs):
    card_to_update = db.query(Card).filter(Card.card_id == card_id, Card.facility_code == facility_code).first()
    
    if not card_to_update:
        raise ValueError("Card not found.")

    for key, value in kwargs.items():
        if hasattr(card_to_update, key):
            setattr(card_to_update, key, value)
    
    db.commit()
    db.refresh(card_to_update)
    return card_to_update

def delete_card(db: Session, card_id: str, facility_code: int):
    card_to_delete = db.query(Card).filter(Card.card_id == card_id, Card.facility_code == facility_code).first()

    if not card_to_delete:
        raise ValueError("Card not found.")
    
    db.delete(card_to_delete)
    db.commit()
    return card_to_delete

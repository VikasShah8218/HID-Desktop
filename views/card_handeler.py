from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import Card
from hid import write_command

def add_card_to_db(db: Session, card_id: str, facility_code: int, issue_code: int, cardholder_name: str, cardholder_phone_no: str, alvl: str = None):
    existing_card = db.query(Card).filter(Card.card_id == card_id, Card.facility_code == facility_code).first()
    
    if existing_card:
        return False, "Card with the same card_id and facility_code already exists."
    try:
        new_card = Card(
            card_id=card_id,
            facility_code=facility_code,
            issue_code=issue_code,
            card_holder_name=cardholder_name,
            card_holder_phone_no=cardholder_phone_no,
            alvl=alvl
        )
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        return True, f"Card {card_id} added successfully."
    except IntegrityError:
        db.rollback()
        return False, "Failed to add the card due to a database error."
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}"

def card_test(db: Session, card_id: str, facility_code: int, acr_number: int=None):
    existing_card = db.query(Card).filter(Card.card_id == card_id, Card.facility_code == facility_code).first()

    if existing_card:
        # return False, "Card with the same card_id and facility_code already exists."
        try:
            if(write_command("331 1234 1 1 -1 1 6 50001 -1")):
                return True, f"card Simulated"
        except IntegrityError:
            db.rollback()
            return False, "Failed to add the card due to a database error."
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
    else:
        return False, "something Went wrong "

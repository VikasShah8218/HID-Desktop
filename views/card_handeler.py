from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import Card
from controller.hid import write_command
from  database.database import get_db

db: Session = next(get_db())

def add_card_to_db(db: Session, card_id: str, facility_code: int, issue_code: int, cardholder_name: str, cardholder_phone_no: str, alvl: str = None):
    existing_card = db.query(Card).filter(Card.card_id == card_id, Card.facility_code == facility_code).first()
    card_pin = "1234"
    if existing_card:
        return False, "Card with the same card_id and facility_code already exists."
    try:
        command = f'5304 0 1234 1 {card_id} -1 "{card_pin}" 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1651363201 2085978495 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
        if (write_command(command)):
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
        else:
            return False, f"Something went wrong with controller."
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
            if(write_command(f"331 1234 1 {acr_number} -1 1 6 {existing_card.card_id} -1")):
                return True, f"card Simulated"
            else:
                return (False, "Something went wrong with Controller")
        except IntegrityError:
            db.rollback()
            return False, "Failed to add the card due to a database error."
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
    else:
        return False, "Card Not Found"

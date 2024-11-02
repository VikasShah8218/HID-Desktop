from sqlalchemy.orm import Session
from database.models import Controller
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from database.database import get_db


db: Session = next(get_db())


def create_controller(name: str, scp_number: int, channel_number: int, ip: str):
    try:
        new_controller = Controller(
            name=name,
            scp_number=scp_number,
            channel_number=channel_number,
            ip=ip
        )
        db.add(new_controller)
        db.commit()
        db.refresh(new_controller)
        return True, new_controller
    except IntegrityError as e:
        db.rollback()
        print("Error: A controller with this SCP number, channel number, or IP already exists.")
        msg = "A controller with this SCP number, channel number, or IP already exists."
        return False,msg
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return False,str(e)

def get_controllers(skip: int = 0, limit: int = 10):
    return db.query(Controller).offset(skip).limit(limit).all()

def get_controller(controller_id: int=None,scp_number:int=None) -> Controller:
    try:
        if controller_id:
            controller_record = db.query(Controller).filter(Controller.id == controller_id).first()
        elif scp_number:
            controller_record = db.query(Controller).filter(Controller.scp_number == scp_number).first()

        if not controller_record:
            print(f"Controller with ID {controller_id} does not exist.")
            return None , f"Controller with ID {controller_id} does not exist."
        return controller_record

    except SQLAlchemyError as e:
        print(f"An error occurred while retrieving the controller: {str(e)}")
        return None , f"An error occurred while retrieving the controller: {str(e)}"
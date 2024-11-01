from sqlalchemy.orm import Session
from database.models import Controller
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db


db: Session = next(get_db())

def create_controller(ip: str, scp_number: int, channel_number: int , name: str = "Controller 1"):
    controller = Controller(ip=ip, scp_number=scp_number, channel_number=channel_number,name=name)
    db.add(controller)
    db.commit()
    db.refresh(controller)
    return controller

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
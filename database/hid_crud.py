from sqlalchemy.orm import Session
from .models import Controller


def create_controller(db: Session, ip: str, scp_number: int, channel_number: int , name: str = "Controller 1"):
    controller = Controller(ip=ip, scp_number=scp_number, channel_number=channel_number,name=name)
    db.add(controller)
    db.commit()
    db.refresh(controller)
    return controller

def get_controller(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Controller).offset(skip).limit(limit).all()




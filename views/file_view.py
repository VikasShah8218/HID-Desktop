from sqlalchemy.exc import SQLAlchemyError
from database.models import UploadedFile
from  database.database import get_db
from sqlalchemy.orm import Session


db: Session = next(get_db())
def upload_file(file_name: str, file_content: str, purpose: str = "Default Purpose", notes: str = None):
    db: Session = next(get_db())
    new_file = UploadedFile(file_name=file_name, file_content=file_content, purpose=purpose, notes=notes)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def get_all_files():
    db: Session = next(get_db())
    return db.query(UploadedFile).all()


def get_config_file_by_id(db: Session, file_id: int) -> UploadedFile:
    try:
        file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not file_record:
            print(f"Record with ID {file_id} does not exist.")
            return None
        return file_record
    
    except SQLAlchemyError as e:
        print(f"An error occurred while retrieving the record: {str(e)}")
        return None


def delete_config_record(db: Session, file_id: int) -> str:
    try:
        file_record = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
        if not file_record:
            return f"Record with ID {file_id} does not exist."
        db.delete(file_record)
        db.commit()
        return f"Record with ID {file_id} has been successfully deleted."

    except SQLAlchemyError as e:
        db.rollback()
        return f"An error occurred while trying to delete the record: {str(e)}"

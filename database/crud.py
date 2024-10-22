# crud.py
from sqlalchemy.orm import Session
from models import User

# Create User
def create_user(db: Session, name: str, email: str, hashed_password: str):
    user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Get User by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Get User by Email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get All Users
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# Update User
def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        db.commit()
        db.refresh(user)
    return user

# Delete User
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

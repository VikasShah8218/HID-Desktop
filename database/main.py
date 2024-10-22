# main.py
from database import get_db
from crud import create_user, get_user, get_users, update_user, delete_user
from hid_crud import create_controller,get_controller
from sqlalchemy.orm import Session
import hashlib

def main():
    # Get the database session
    db: Session = next(get_db())
    
    for i in range(6):
        controller = create_controller(db,f"192.168.0.25{i}",1234+i, 257+i,f"Controller {i}")
        print(controller.scp_number, ": Created") 
    
    controllers = get_controller(db)
    for i in controllers:
        print(i.ip, "  " , i.channel_number ,"  " , i.scp_number , "  ", i.name)
    # # Create a user
    # hashed_password = hashlib.sha256("password".encode()).hexdigest()
    # new_user = create_user(db, name="John Doe", email="john@example.com", hashed_password=hashed_password)
    # print(f"User created: {new_user.name}, {new_user.email}")
    
    # # Get a user by ID
    # user = get_user(db, new_user.id)
    # print(f"User fetched: {user.name}, {user.email}")
    
    # # Update a user
    # updated_user = update_user(db, new_user.id, name="Johnny Doe")
    # print(f"User updated: {updated_user.name}")
    
    # # Get all users
    # all_users = get_users(db)
    # print(f"All users: {[(user.name, user.email) for user in all_users]}")
    
    # # Delete a user
    # delete_user(db, new_user.id)
    # print(f"User {new_user.id} deleted")


if __name__ == "__main__":
    main()

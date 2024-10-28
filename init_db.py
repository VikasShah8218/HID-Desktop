from database.database import engine
from database.models import Base

# This will create the tables defined in models.py
# Base.metadata.create_all(bind=engine)

# Drop all tables and recreate them
# Base.metadata.drop_all(bind=engine)  # Drops all tables
Base.metadata.create_all(bind=engine)  # Recreates tables



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection_db = "postgresql://postgres:admin@localhost:5432/flask_db"
connection_db = "postgresql://igqhpsbklssawn:434ae956ad3a604d715c994180696d4a1b5d3c8f024a273971f572ba1c4aadd9@ec2-34-234-240-121.compute-1.amazonaws.com:5432/d3iffjku1liua3"

Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)
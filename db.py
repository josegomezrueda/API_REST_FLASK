
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection_db = "postgresql://postgres:admin@localhost:5432/flask_db"
connection_db = "postgresql://dzzjehwhljgrqd:c2daab1612c9f5b82a2f432c91969d01e0aade35ac69cae9f2371fe2aa105188@ec2-52-49-120-150.eu-west-1.compute.amazonaws.com:5432/d1o747k2054ltn"

Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)
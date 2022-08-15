
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection_db = "postgresql://postgres:admin@localhost:5432/flask_db"
connection_db = "postgresql://aucpqrekjkslfu:106ac53ecc7ac7ea7806f80c0f7c6aa70ec43593c0dcad4b935db9f77a7f1a13@ec2-54-228-218-84.eu-west-1.compute.amazonaws.com:5432/d92gluid5qr66u"

Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)
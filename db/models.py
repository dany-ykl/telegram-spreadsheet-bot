from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(100))  


    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email    

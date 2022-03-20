from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models import Users


class DB:


    def __init__(self):
        self.engine = create_engine('sqlite:///db/data.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_user(self, user_id):
        user = self.session.query(Users).get(user_id)
        user_data = {'user_id': user.user_id, 'email':user.email}
        return  user_data

    def add_user(self, user_id, email):
        user = Users(user_id=user_id, email=email)
        self.session.add(user)
        self.session.commit()
 
    def update_user_email(self, user_id, email):
        user = self.session.query(Users).get(user_id)
        user.email = email
        self.session.commit()

    def delete_user(self, user_id):
        user = self.session.query(Users).get(user_id)
        self.session.delete(user)
        self.session.commit()
        

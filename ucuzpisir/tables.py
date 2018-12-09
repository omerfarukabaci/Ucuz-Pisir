import psycopg2 as dbapi2
import os
from datetime import datetime
from flask import current_app as app
from ucuzpisir import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = User("1", "2", "3", " " )
    return user.retrieve('user_id', user_id)[0] #Check this

class Base:
    def __init__(self):
        self.connection_url = app.config["DATABASE_URI"]

    def create(self):
        pass

    def update(self):
        pass

    def retrieve(self):
        pass

    def delete(self):
        pass

    def execute(self, statement, fetch=False):
        response = None
        with dbapi2.connect(self.connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                if fetch:
                    response = cursor.fetchall()
        return response

class User(Base, UserMixin):

    def __init__(self, name = None, username = None, email = None, password = None, birthdate=None, pic="imgs/defaultProfile.jpg"):
        super(User, self).__init__()  # check
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = birthdate
        self.pic = pic

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pic}')"

    def create(self):
        statement = f"""
        insert into users (name, username, password, email, pic, birthdate)
        values ('{self.name}', '{self.username}', '{self.password}', '{self.email}', '{self.pic}', '{self.birthdate}')
        """
        self.execute(statement)

    def update(self):
        statement = """
        temp
        """
        self.execute(statement)

    def retrieve(self, queryKey, condition=None):
        statement = f"""
        select {queryKey} from users"""
        if (condition):
            statement += f""" 
            where {condition}
            """
        return self.execute(statement, fetch=True)

    def delete(self):
        statement = """
        temp
        """
        self.execute(statement)


class Recipe(Base):
    def __init__(self, user_id, title, recipe_text, ingridients, date_posted=datetime.utcnow,  # Fix datetime
                 recipe_img="imgs/defaultRecipe.jpg"):
        self.user_id = user_id
        self.title = title
        self.recipe_text = recipe_text
        self.ingridients = ingridients
        self.date_posted = date_posted
        self.recipe_img = recipe_img

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def create(self):
        statement = """
        temp
        """
        self.execute(statement)

    def update(self):
        statement = """
        temp
        """
        self.execute(statement)

    def retrieve(self):
        statement = """
        temp
        """
        return self.execute(statement)

    def delete(self):
        statement = """
        temp
        """
        self.execute(statement)

import psycopg2 as dbapi2
import os
from datetime import datetime
from flask import current_app as app
from ucuzpisir import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    userData = User().retrieve('*', f"user_id = {user_id}")
    if userData:
        user = User(user_id=userData[0][0], name=userData[0][1], username=userData[0][2],
                    password=userData[0][3], email=userData[0][4],
                    pic=userData[0][5], birthdate=userData[0][6])
    else:
        user = None
    return user


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

    def __init__(self, user_id=None, name=None, username=None,
                 email=None, password=None, birthdate=None, pic="default_user.jpg"):
        super(User, self).__init__()  # check
        self.user_id = user_id
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
        values ('{self.name}', '{self.username}', '{self.password}', '{self.email}',
        '{self.pic}', '{self.birthdate}')
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update users 
        set name ='{self.name}', username='{self.username}', email='{self.email}',
        pic='{self.pic}', birthdate='{self.birthdate}'
        where user_id = {self.user_id}
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

    def get_id(self):
        return str(self.user_id)


class Recipe(Base):
    def __init__(self, user_id, title, recipe_text, ingridients,
                 date_posted=datetime.utcnow,  # Fix datetime
                 recipe_img="imgs/defaultRecipe.jpg"):
        self.user_id = user_id
        self.title = title
        self.recipe_text = recipe_text
        self.ingridients = ingridients
        self.date_posted = date_posted
        self.recipe_img = recipe_img

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class User_image(Base):
    def __init__(self, img_id = None, filename = None, extension = None, img_data = None,
                 date_uploaded = None, user_id = None):
        self.img_id = img_id
        self.filename = filename
        self.extension = extension 
        self.img_data = img_data 
        self.date_uploaded = date_uploaded
        self.user_id = user_id
    def __repr__(self):
        return f"Post('{self.filename}', '{self.date_uploaded}')"

    def create(self):
        statement = f"""
        insert into user_images (filename, extension, img_data, user_id)
        values ('{self.filename}', '{self.extension}', '{self.img_data}', {self.user_id})
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update user_images 
        set filename ='{self.filename}', extension='{self.extension}', img_data='{self.img_data}'
        where user_id = {self.user_id}
        """
        self.execute(statement)

    def retrieve(self, queryKey, condition):
        statement = f"""
        select {queryKey} from user_images"""
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

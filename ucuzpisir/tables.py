import psycopg2 as dbapi2
import os
from datetime import datetime

class Base:
    def __init__(self):
        self.connection_url = os.getenv("DATABASE_URL")

    def create(self):
        pass

    def update(self):
        pass

    def retrieve(self):
        pass

    def delete(self):
        pass

    def execute(self, statement):
        response = None
        with dbapi2.connect(self.connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                response = cursor.fetchall()
        return response


class User(Base):
    def __init__(self, username, email, password, birthdate=None, pic="imgs/defaultProfile.jpg"):
        #super(User, self).__init__()  # check
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = birthdate
        self.pic = pic

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pic}')"

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

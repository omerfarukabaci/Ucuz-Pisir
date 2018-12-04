#import ??
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
    __init__(self, user_id, username, email, password, birthdate, 
                pic=url_for('static', filename="imgs/defaultProfile.jpg")):
        user_id = user_id
        username = username
        email = email
        password = password
        birthdate = birthdate
        pic = pic

    __repr__(self):
        return f"User('{self.username}', '{self.email}')"

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
    __init__(self, user_id, title, recipe_text, ingridients, date_posted,
                recipe_img=url_for('static', filename="imgs/defaultRecipe.jpg")):
        user_id = user_id
        title = title
        recipe_text = recipe_text
        ingridients = ingridients
        date_posted = date_posted
        recipe_img = recipe_img

    __repr__():
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

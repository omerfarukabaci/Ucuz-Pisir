#import ??


class User:
    __init__(self, user_id, username, email, password, birthdate, 
            pic=url_for('static', filename="imgs/"+recipe.image_path)):
        user_id = user_id;
        username = username;
        email = email;
        password = password;
        birthdate = birthdate;
        pic = pic;

    __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Recipe:
    __init__(self, user_id, recipe_text, ingridients):
        user_id = user_id;
        recipe_text = recipe_text;
        ingridients = ingridients;
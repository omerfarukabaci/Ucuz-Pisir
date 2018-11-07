#import ??


class User:
    __init__(self, user_id, username, email, password, birthdate, 
                pic=url_for('static', filename="imgs/defaultProfile.jpg")):
        user_id = user_id;
        username = username;
        email = email;
        password = password;
        birthdate = birthdate;
        pic = pic;

    __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Recipe:
    __init__(self, user_id, title, recipe_text, ingridients, date_posted,
                recipe_img=url_for('static', filename="imgs/defaultRecipe.jpg)):
        user_id = user_id;
        title = title;
        recipe_text = recipe_text;
        ingridients = ingridients;
        date_posted = date_posted;
        recipe_img = recipe_img
    __repr__():
        return f"Post('{self.title}', '{self.date_posted}')"
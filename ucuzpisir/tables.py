import psycopg2 as dbapi2
import io
from flask import current_app as app
from ucuzpisir import login_manager
from flask_login import UserMixin
from PIL import Image, ImageOps, ExifTags


@login_manager.user_loader
def load_user(user_id):
    users = User().retrieve('*', f"user_id = {user_id}")
    if users:
        user = users[0]
    else:
        user = None
    return user


class Base:
    def __init__(self, url=None):
        if url:
            self.connection_url = url
        else:
            self.connection_url = app.config["DATABASE_URI"]

    def create(self):
        pass

    def update(self):
        pass

    def retrieve(self):
        pass

    def delete(self):
        pass

    def execute(self, statement, variables=None, fetch=False):
        response = None
        with dbapi2.connect(self.connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, variables)
                if fetch:
                    response = cursor.fetchall()
        return response

    def join(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from users
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        query = self.execute(statement, variables, fetch=True)
        return query


class User(Base, UserMixin):

    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, birthdate=None, img_id=1):
        super(User, self).__init__()
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = birthdate
        self.img_id = img_id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}')"

    def create(self):
        statement = """
        insert into users (name, username, password, email, img_id, birthdate)
        values (%s, %s, %s, %s, %s, %s)
        """
        self.execute(statement, (self.name, self.username, self.password, self.email, self.img_id, self.birthdate))

    def update(self):
        statement = """
        update users
        set name = %s, username = %s, email = %s,
        img_id = %s, birthdate = %s
        where user_id = %s
        """
        self.execute(statement, (self.name, self.username, self.email, self.img_id, self.birthdate, self.user_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from users"""
        if (condition):
            statement += f"""
            where {condition}
            """
        user_datas = self.execute(statement, variables, fetch=True)
        if query_key == '*':
            users = []
            for user_data in user_datas:
                user = User(user_id=user_data[0], name=user_data[1], username=user_data[2],
                            password=user_data[3], email=user_data[4],
                            birthdate=user_data[5], img_id=user_data[6])
                users.append(user)
            return users
        return user_datas

    def delete(self):
        statement = """
        temp
        """
        self.execute(statement)

    def get_id(self):
        return str(self.user_id)


class Recipe(Base):
    def __init__(self, recipe_id=None, title=None, content=None, date_posted=None, author_id=None, img_id=1):
        super(Recipe, self).__init__()
        self.recipe_id = recipe_id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.author_id = author_id
        self.img_id = img_id

    def create(self):
        statement = """
        insert into recipes (title, content, img_id, author_id)
        values (%s, %s, %s, %s)
        """
        self.execute(statement, (self.title, self.content,
                                 self.img_id, self.author_id))

    def update(self):
        statement = """
        update recipes
        set title = %s, content = %s, img_id = %s
        where recipe_id = %s
        """
        self.execute(statement, (self.title, self.content,
                                 self.img_id, self.recipe_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"select {query_key} from recipes"
        if (condition):
            statement += f"""
            where {condition}
            """
        recipe_datas = self.execute(statement, variables, fetch=True)

        if query_key == '*':
            recipes = []
            for recipe_data in recipe_datas:
                recipe = Recipe(
                    recipe_id=recipe_data[0],
                    title=recipe_data[1],
                    content=recipe_data[2],
                    date_posted=recipe_data[3],
                    img_id=recipe_data[4],
                    author_id=recipe_data[5]
                )
                recipes.append(recipe)
            return recipes
        return recipe_datas

    def delete(self):
        statement = """
        delete from recipes
        where recipe_id = %s
        """
        self.execute(statement, (self.recipe_id,))

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.date_posted}')"


class ImageBase(Base):
    def __init__(self, url=None, img_id=None, filename=None, extension=None, img_data=None, date_uploaded=None):
        super(ImageBase, self).__init__(url=url)
        self.img_id = img_id
        self.filename = filename
        self.extension = extension
        self.img_data = img_data
        self.date_uploaded = date_uploaded

    def __repr__(self):
        return f"Image('{self.filename}', '{self.date_uploaded}')"

    def reformat_image(self, size=(125, 125)):
        if self.filename is None:
            return
        img = Image.open(self.img_data)
        img = self.correct_image_rotation(img)
        img = ImageOps.fit(img, size, Image.ANTIALIAS)
        output = io.BytesIO()
        img.save(output, format=self.extension)
        self.img_data = output.getvalue()

    def correct_image_rotation(self, image):
        if hasattr(image, '_getexif'):
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif_data = image._getexif()
            if exif_data is not None:
                exif = dict(exif_data.items())
                orientation = exif[orientation]
                if orientation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    image = image.transpose(Image.ROTATE_90)
        return image


class UserImage(ImageBase):
    def __init__(self, url=None, img_id=None, filename=None, extension=None, img_data=None, date_uploaded=None):
        super(UserImage, self).__init__(
            img_id=img_id,
            filename=filename,
            extension=extension,
            img_data=img_data,
            date_uploaded=date_uploaded,
            url=url
        )
        self.reformat_image()

    def create(self):
        statement = """
        insert into user_images (filename, extension, img_data)
        values (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """
        self.execute(statement, (self.filename, self.extension, dbapi2.Binary(self.img_data)))

    def update(self):
        statement = """
        update user_images
        set filename = %s, extension = %s, img_data = %s
        where img_id = %s
        """
        self.execute(statement, (self.filename, self.extension, self.img_data, self.img_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from user_images"""
        if (condition):
            statement += f"""
            where {condition}
            """
        image_datas = self.execute(statement, variables, fetch=True)
        if query_key == '*':
            images = []
            for image_data in image_datas:
                image = UserImage(img_id=image_data[0], extension=image_data[2], img_data=image_data[3], date_uploaded=image_data[4])
                images.append(image)
            return images
        return image_datas

    def delete(self, img_id):
        statement = """
        delete from user_images
        where img_id = %s
        """
        self.execute(statement, (img_id,))


class RecipeImage(ImageBase):
    def __init__(self, url=None, img_id=None, filename=None, extension=None, img_data=None, date_uploaded=None):
        super(RecipeImage, self).__init__(
            img_id=img_id,
            filename=filename,
            extension=extension,
            img_data=img_data,
            date_uploaded=date_uploaded,
            url=url
        )
        self.reformat_image(size=(300, 300))

    def create(self):
        statement = """
        insert into recipe_images (filename, extension, img_data)
        values (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """
        self.execute(statement, (self.filename, self.extension, dbapi2.Binary(self.img_data)))

    def update(self):
        statement = """
        update recipe_images
        set filename = %s, extension = %s, img_data = %s
        where img_id = %s
        """
        self.execute(statement, (self.filename, self.extension, self.img_data, self.img_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from recipe_images
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        image_datas = self.execute(statement, variables, fetch=True)
        if query_key == '*':
            images = []
            for image_data in image_datas:
                image = RecipeImage(img_id=image_data[0], extension=image_data[2], img_data=image_data[3], date_uploaded=image_data[4])
                images.append(image)
            return images
        return image_datas

    def delete(self, img_id):
        statement = """
        delete from recipe_images
        where img_id = %s
        """
        self.execute(statement, (img_id,))


class Ingredient(Base):
    def __init__(self, ingredient_id=None, name=None, calories=None, protein=None, fat=None, carb=None):
        super(Ingredient, self).__init__()
        self.ingredient_id = ingredient_id
        self.name = name
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.carb = carb

    def create(self):
        statement = """
        insert into ingredients (name, calories, protein, fat, carb)
        values (%s, %s, %s, %s, %s)
        """
        self.execute(statement, (self.name, self.calories, self.protein, self.fat, self.carb))

    def update(self):
        statement = """
        update ingredients
        set name = %s, calories = %s,
        protein = %s, fat = %s, carb = %s
        where user_id = %s
        """
        self.execute(statement, (self.name, self.calories, self.protein, self.fat, self.carb, self.ingredient_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from ingredients
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        ingredient_datas = self.execute(statement, variables, fetch=True)
        if query_key == '*':
            ingredients = []
            for ingredient_data in ingredient_datas:
                ingredient = Ingredient(
                    ingredient_id=ingredient_data[0],
                    name=ingredient_data[1],
                    calories=ingredient_data[2],
                    protein=ingredient_data[3],
                    fat=ingredient_data[4],
                    carb=ingredient_data[5]
                )
                ingredients.append(ingredient)
            return ingredients
        return ingredient_datas

    def delete(self):
        statement = """
        delete from ingredients
        where ingredient_id = %s
        """
        self.execute(statement, (self.ingredient_id,))


class RecipeIngredient(Base):
    def __init__(self, recipe_id=None, ingredient_id=None, quantity=None, unit=None):
        super(RecipeIngredient, self).__init__()
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.unit = unit

    def create(self):
        statement = """
        insert into recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
        values (%s, %s, %s, %s)
        """
        self.execute(statement, (self.recipe_id, self.ingredient_id, self.quantity, self.unit))

    def update(self):
        statement = """
        update recipe_ingredients
        set recipe_id = %s, ingredient_id = %s, quantity = %s, unit = %s
        where recipe_id = %s and ingredient_id = %s
        """
        self.execute(statement, (self.recipe_id, self.ingredient_id,
                                 self.quantity, self.unit,
                                 self.recipe_id, self.ingredient_id))

    def retrieve(self, query_key, condition=None, variables=None):
        statement = f"""
        select {query_key} from recipe_ingredients
        """
        if (condition):
            statement += f"""
            where {condition}
            """
        recipe_ingredient_datas = self.execute(
            statement, variables, fetch=True)
        if query_key == '*':
            recipe_ingredients = []
            for recipe_ingredient_data in recipe_ingredient_datas:
                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe_ingredient_data[0],
                    ingredient_id=recipe_ingredient_data[1],
                    quantity=recipe_ingredient_data[2],
                    unit=recipe_ingredient_data[3]
                )
                recipe_ingredients.append(recipe_ingredient)
            return recipe_ingredients
        return recipe_ingredient_datas

    def delete(self):
        statement = """
        delete from recipe_ingredients
        where recipe_id = %s and ingredient_id = %s
        """
        self.execute(statement, (self.recipe_id, self.ingredient_id))

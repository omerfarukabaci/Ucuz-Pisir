import psycopg2 as dbapi2
import os
import io
from datetime import datetime
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
                 email=None, password=None, birthdate=None, img_id=1):
        super(User, self).__init__()  # check
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
        statement = f"""
        insert into users (name, username, password, email, img_id, birthdate)
        values ('{self.name}', '{self.username}', '{self.password}', '{self.email}',
        '{self.img_id}', '{self.birthdate}')
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update users 
        set name ='{self.name}', username='{self.username}', email='{self.email}',
        img_id={self.img_id}, birthdate='{self.birthdate}'
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
        userDatas = self.execute(statement, fetch=True)
        users = []
        for userData in userDatas:
            user = User(user_id=userData[0], name=userData[1], username=userData[2],
                        password=userData[3], email=userData[4],
                        birthdate=userData[5], img_id=userData[6])
            users.append(user)

        return users

    def delete(self):
        statement = """
        temp
        """
        self.execute(statement)

    def get_id(self):
        return str(self.user_id)


class Recipe(Base):
    def __init__(self, recipe_id=None, title=None, content=None,
                 date_posted=None, author_id=None,
                 img_id=1):
        super(Recipe, self).__init__() 
        self.recipe_id = recipe_id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.author_id = author_id
        self.img_id = img_id
    
    def create(self):
        statement = f"""
        insert into recipes (title, content, img_id, author_id)
        values ('{self.title}', '{self.content}', '{self.img_id}',
        '{self.author_id}')
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update recipes 
        set title ='{self.title}', content='{self.content}', img_id={self.img_id}'
        where recipe_id = {self.recipe_id}
        """
        self.execute(statement)

    def retrieve(self, queryKey, condition=None):
        statement = f"""
        select {queryKey} from recipes"""
        if (condition):
            statement += f""" 
            where {condition}
            """
        recipeDatas = self.execute(statement, fetch=True)
        recipes = []
        for recipeData in recipeDatas:
            recipe = Recipe(recipe_id=recipeData[0], title=recipeData[1], content=recipeData[2],
                            date_posted=recipeData[3], img_id=recipeData[4], author_id=recipeData[5])
            recipes.append(recipe)

        return recipes

    def delete(self):
        statement = f"""
        delete from recipes
        where recipe_id = {self.recipe_id}
        """
        self.execute(statement)


    def __repr__(self):
        return f"Recipe('{self.title}', '{self.date_posted}')"


class ImageBase(Base):
    def __init__(self, url=None, img_id=None, filename=None, extension=None,
                img_data=None, date_uploaded=None):
        super(ImageBase, self).__init__(url=url)
        self.img_id = img_id
        self.filename = filename
        self.extension = extension
        self.img_data = img_data
        self.date_uploaded = date_uploaded

    def __repr__(self):
        return f"Image('{self.filename}', '{self.date_uploaded}')"

    def reformatImage(self, size=(125, 125)):
        if self.filename == None:
            return
        img = Image.open(self.img_data)
        img = self.correctImageRotation(img)
        img = ImageOps.fit(img, size, Image.ANTIALIAS)
        output = io.BytesIO()
        img.save(output, format=self.extension)
        self.img_data = output.getvalue()

    def correctImageRotation(self, image):
        if hasattr(image, '_getexif'):
            for orientation in ExifTags.TAGS.keys(): 
                if ExifTags.TAGS[orientation]=='Orientation':
                    break 
            exifData = image._getexif()
            if exifData is not None:
                exif=dict(exifData.items())
                orientation = exif[orientation] 
                if orientation == 3:   image = image.transpose(Image.ROTATE_180)
                elif orientation == 6: image = image.transpose(Image.ROTATE_270)
                elif orientation == 8: image = image.transpose(Image.ROTATE_90)
        return image


class User_image(ImageBase):
    def __init__(self, url=None, img_id=None, filename=None, extension=None, img_data=None,
                 date_uploaded=None):
        super(User_image, self).__init__(img_id=img_id, filename=filename,
                                        extension=extension,img_data=img_data,
                                        date_uploaded=date_uploaded, url=url)
        self.reformatImage()

    def create(self):
        statement = f"""
        insert into user_images (filename, extension, img_data)
        values ('{self.filename}', '{self.extension}', {dbapi2.Binary(self.img_data)})
        ON CONFLICT DO NOTHING
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update user_images 
        set filename ='{self.filename}', extension='{self.extension}', img_data='{self.img_data}'
        where img_id = {self.img_id}
        """
        self.execute(statement)

    def retrieve(self, queryKey, condition=None):
        statement = f"""
        select {queryKey} from user_images"""
        if (condition):
            statement += f""" 
            where {condition}
            """
        imageDatas = self.execute(statement, fetch=True)
        images = []
        for imageData in imageDatas:
            image = User_image(img_id=imageData[0], extension=imageData[2],
            img_data=imageData[3], date_uploaded=imageData[4])
            images.append(image)

        return images

    def delete(self, img_id):
        statement = f"""
        delete from user_images
        where img_id = {img_id}
        """
        self.execute(statement)

class Recipe_image(ImageBase):
    def __init__(self, url=None, img_id=None, filename=None, extension=None, img_data=None,
                 date_uploaded=None):
        super(Recipe_image, self).__init__(img_id=img_id, filename=filename,
                                        extension=extension,img_data=img_data,
                                        date_uploaded=date_uploaded, url=url)
        self.reformatImage(size=(300, 300))

    def create(self):
        statement = f"""
        insert into recipe_images (filename, extension, img_data)
        values ('{self.filename}', '{self.extension}', {dbapi2.Binary(self.img_data)})
        ON CONFLICT DO NOTHING
        """
        self.execute(statement)

    def update(self):
        statement = f"""
        update recipe_images 
        set filename ='{self.filename}', extension='{self.extension}', img_data='{self.img_data}'
        where img_id = {self.img_id}
        """
        self.execute(statement)

    def retrieve(self, queryKey, condition=None):
        statement = f"""
        select {queryKey} from recipe_images"""
        if (condition):
            statement += f""" 
            where {condition}
            """
        imageDatas = self.execute(statement, fetch=True)
        images = []
        for imageData in imageDatas:
            image = Recipe_image(img_id=imageData[0], filename=None,
                    extension=imageData[2], img_data=imageData[3],
                    date_uploaded=imageData[4])
            images.append(image)

        return images

    def delete(self, img_id):
        statement = f"""
        delete from recipe_images
        where img_id = {img_id}
        """
        self.execute(statement)


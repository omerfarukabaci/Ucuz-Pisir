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
    userData = User().retrieve('*', f"user_id = {user_id}")
    if userData:
        user = User(user_id=userData[0][0], name=userData[0][1], username=userData[0][2],
                    password=userData[0][3], email=userData[0][4],
                     birthdate=userData[0][5], img_id=userData[0][6])
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
        img_id='{self.img_id}', birthdate='{self.birthdate}'
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
    def __init__(self, recipe_id, title, content,
                 date_posted=datetime.utcnow,
                 recipe_img="imgs/defaultRecipe.jpg"):
        super(Recipe, self).__init__() 
        self.recipe_id = recipe_id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.recipe_img = recipe_img
    #necessary functions will be written below

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
        return self.execute(statement, fetch=True)

    def delete(self, img_id):
        statement = f"""
        delete from user_images
        where img_id = {img_id}
        """
        self.execute(statement)
import os
import sys
import psycopg2 as dbapi2
from ucuzpisir.tables import User_image, Recipe_image

INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS USER_IMAGES(
        IMG_ID SERIAL PRIMARY KEY,
        FILENAME VARCHAR(20) UNIQUE NOT NULL,
        EXTENSION VARCHAR(7) NOT NULL,
        IMG_DATA BYTEA NOT NULL,
        DATE_UPLOADED DATE DEFAULT CURRENT_DATE
    )
    """,
        """CREATE TABLE IF NOT EXISTS RECIPE_IMAGES(
        IMG_ID SERIAL PRIMARY KEY,
        FILENAME VARCHAR(20) UNIQUE NOT NULL,
        EXTENSION VARCHAR(7) NOT NULL,
        IMG_DATA BYTEA NOT NULL,
        DATE_UPLOADED DATE DEFAULT CURRENT_DATE
    )
    """,
    """CREATE TABLE IF NOT EXISTS USERS(
        USER_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        USERNAME VARCHAR(50) UNIQUE NOT NULL,
        PASSWORD VARCHAR(70) NOT NULL,
        EMAIL VARCHAR(80) UNIQUE NOT NULL,
        BIRTHDATE DATE,
        IMG_ID INTEGER REFERENCES USER_IMAGES(IMG_ID) ON DELETE SET DEFAULT DEFAULT 1
    )
    """,
    """CREATE TABLE IF NOT EXISTS RECIPES(
        RECIPE_ID SERIAL PRIMARY KEY,
        TITLE VARCHAR(50) NOT NULL,
        CONTENT TEXT NOT NULL,
        DATE_POSTED DATE DEFAULT CURRENT_DATE,
        IMG_ID INTEGER REFERENCES RECIPE_IMAGES(IMG_ID) ON DELETE SET DEFAULT DEFAULT 1,
        AUTHOR_ID INTEGER REFERENCES USERS(USER_ID) 
    )
    """,
    """CREATE TABLE IF NOT EXISTS INGREDIENTS(
        INGREDIENT_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) UNIQUE NOT NULL,
        CALORIES INTEGER NOT NULL,
        PROTEIN INTEGER NOT NULL,
        FAT INTEGER NOT NULL,
        CARB INTEGER NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS RECIPE_INGREDIENTS(
        RECIPE_ID INTEGER REFERENCES RECIPES(RECIPE_ID) ON DELETE CASCADE,
        INGREDIENT_ID INTEGER REFERENCES INGREDIENTS(INGREDIENT_ID) ON DELETE CASCADE,
        QUANTITY INTEGER NOT NULL,
        UNIT VARCHAR(10) NOT NULL,
        PRIMARY KEY (RECIPE_ID, INGREDIENT_ID)
    )
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()
    insertDefaultImages(url)


def insertDefaultImages(url):
    with open('ucuzpisir/static/imgs/default_user.jpg', 'rb') as f:
        imageData = f
        defaultImage = User_image(url=url, filename='default', extension='jpeg',
                                  img_data=imageData)
        defaultImage.create()

    with open('ucuzpisir/static/imgs/default_recipe.jpg', 'rb') as f:
        imageData = f
        defaultImage = Recipe_image(url=url, filename='default', extension='jpeg',
                                  img_data=imageData)
        defaultImage.create()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

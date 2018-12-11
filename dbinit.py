import os
import sys
import psycopg2 as dbapi2
from ucuzpisir.tables import User_image

INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS USER_IMAGES(
        IMG_ID SERIAL PRIMARY KEY,
        FILENAME VARCHAR(20) UNIQUE NOT NULL,
        EXTENSION VARCHAR(7) NOT NULL,
        IMG_DATA BYTEA NOT NULL,
        DATE_UPLOADED DATE DEFAULT current_date
    )
    """,
    """CREATE TABLE IF NOT EXISTS USERS(
        USER_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        USERNAME VARCHAR(50) UNIQUE NOT NULL,
        PASSWORD VARCHAR(70) NOT NULL,
        EMAIL VARCHAR(80) UNIQUE NOT NULL,
        BIRTHDATE DATE,
        IMG_ID INTEGER REFERENCES USER_IMAGES(IMG_ID) DEFAULT 1
    )
    """,
    """CREATE TABLE IF NOT EXISTS RECIPES(
        RECIPE_ID SERIAL PRIMARY KEY,
        TITLE VARCHAR(80) NOT NULL,
        CONTENT TEXT NOT NULL,
        PIC VARCHAR(20) DEFAULT 'defaultRecipe.jpg',
        DATE_POSTED TIMESTAMP,
        USER_ID INTEGER REFERENCES USERS(USER_ID)
    )
    """
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()
    insertDefaultImage(url)

def insertDefaultImage(url):
    imageData = open('ucuzpisir/static/imgs/default_user.jpg', 'rb').read()
    defaultImage = User_image(url = url, filename='default', extension='jpg',
                            img_data=imageData)
    defaultImage.create()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

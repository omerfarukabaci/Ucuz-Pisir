import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE USER(
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR(20) UNIQUE NOT NULL,
        PASSWORD VARCHAR(60) NOT NULL,
        EMAIL VARCHAR(80) UNIQUE NOT NULL,
        PIC VARCHAR(20) DEFAULT 'defaultProfile.jpg',
        BIRTHDATE DATE
    )
    """,
    """CREATE TABLE RECIPE(
        ID SERIAL PRIMARY KEY,
        TITLE VARCHAR(80) NOT NULL,
        CONTENT TEXT NOT NULL,
        PIC VARCHAR(20) DEFAULT 'defaultRecipe.jpg'
        DATE_POSTED TIMESTAMP,
        USER_ID INTEGER REFERENCES USER(ID)
    )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

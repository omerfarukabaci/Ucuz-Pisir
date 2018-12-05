from ucuzpisir import app
import os

app.config["DATABASE_URI"] = os.getenv("DATABASE_URL")

if __name__ == "__main__":
    app.run()

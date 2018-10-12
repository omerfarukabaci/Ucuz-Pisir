from flask import Flask


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Testing the heroku auto deploy..."


if __name__ == "__main__":
    app.run()

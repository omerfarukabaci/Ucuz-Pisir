from flask import Flask


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Testing222..."


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, url_for


app = Flask(__name__)

recipes = [
    {
        'title': 'Sushi',
        'image_path': '1.jpg'
    },
    {
        'title': 'Ratatouille',
        'image_path': '2.jpg'
    },
    {
        'title': 'Fish & Chips',
        'image_path': '3.jpg'
    },
    {
        'title': 'New York Steak',
        'image_path': '4.jpg'
    },
    {
        'title': 'Kung Pao Chicken',
        'image_path': '5.jpg'
    },{
        'title': 'Beef Stroganoff',
        'image_path': '6.jpg'
    },
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', recipes = recipes)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

if __name__ == "__main__":
    app.run()

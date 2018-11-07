from flask import render_template, url_for, flash, redirect
from ucuzpisir import app
from ucuzpisir.forms import RegistrationForm, LoginForm
""" import dbase here"""

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
    },
    {
        'title': 'Beef Stroganoff',
        'image_path': '6.jpg'
    },
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
    },
    {
        'title': 'Beef Stroganoff',
        'image_path': '6.jpg'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', content = recipes)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
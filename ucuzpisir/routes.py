from flask import render_template, url_for, flash, redirect
from ucuzpisir import app, bcrypt
from ucuzpisir.forms import RegistrationForm, LoginForm
from ucuzpisir.tables import Base, User

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
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, password=hashedPassword, email=form.email.data, birthdate=form.birthdate.data)
        user.create() #Fix nad control
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print('Error!')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Success!')
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'alert alert-success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    else:
        print('Error!')
    return render_template('login.html', title='Login', form=form)

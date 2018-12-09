from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, password=hashedPassword, email=form.email.data, birthdate=form.birthdate.data)
        user.create() #Fix nad control
        flash(f'Account created for {form.username.data}!', 'alert alert-success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        userData = User().retrieve('*', f"email = '{form.email.data}'")
        if userData:
            user = User(user_id=userData[0][0], name=userData[0][1], username=userData[0][2], password=userData[0][3],
                        email=userData[0][4], pic=userData[0][5], birthdate=userData[0][6])
        else:
            user = None
            
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') 
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check e-mail and password', 'alert alert-danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
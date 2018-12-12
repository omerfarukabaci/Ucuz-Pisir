from os import path
import secrets
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from ucuzpisir import app, bcrypt
from ucuzpisir.forms import RegistrationForm, LoginForm, AccountUpdateForm, RecipeForm
from ucuzpisir.tables import Base, User, User_image, Recipe, Recipe_image


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def home():
    recipeDatas = Recipe().retrieve('*')
    recipes = []
    for recipeData in recipeDatas:
        recipe = Recipe(recipe_id=recipeData[0], title=recipeData[1], content=recipeData[2],
                        date_posted=recipeData[3], img_id=recipeData[4], author_id=recipeData[5])
        recipes.append(recipe)
    return render_template('home.html', recipes=recipes)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data,
                    password=hashedPassword, email=form.email.data, birthdate=form.birthdate.data)
        user.create()  # Fix nad control
        flash(f'Account created for {form.username.data}!',
              'alert alert-success alert-dismissible fade show')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        userData = User().retrieve('*', f"email = '{form.email.data}'")
        if userData:
            user = User(user_id=userData[0][0], name=userData[0][1], username=userData[0][2],
                        password=userData[0][3], email=userData[0][4],
                        birthdate=userData[0][5], img_id=userData[0][6])
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
            flash(f'Login Unsuccessful. Please check e-mail and password',
                  'alert alert-danger alert-dismissible fade show')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    flash(f'Goodbye {current_user.username}!',
          'alert alert-info alert-dismissible fade show')
    logout_user()
    return redirect(url_for('home'))


def createNewImage(form_picture_data, image_type):
    """
    param form_picture_data(image object): picture data from form
    param image_type(string): type of the image, ex: user_image, recipe_image
    returns: id of the created image
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(form_picture_data.filename)
    f_ext = f_ext[1:]
    if f_ext == 'jpg':
        f_ext = 'jpeg'
    if image_type == "User":
        image = User_image(filename=random_hex,
                           extension=f_ext, img_data=form_picture_data)
    elif image_type == "Recipe":
        image = Recipe_image(filename=random_hex,
                             extension=f_ext, img_data=form_picture_data)
    image.create()
    image_id = image.retrieve('*', f"filename = '{random_hex}'")[0][0]
    return image_id


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.img_id != 1:
                User_image().delete(img_id=current_user.img_id)
            current_user.img_id = createNewImage(form.picture.data, "User")
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.birthdate = form.birthdate.data
        current_user.update()  # Fix nad control
        flash(f'Account updated!',
              'alert alert-success alert-dismissible fade show')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.birthdate.data = current_user.birthdate
    image_path = url_for('getUserImage', img_id=current_user.img_id)
    return render_template('account.html', title='Account',
                           image_path=image_path, form=form)


@app.route("/getUserImage/<int:img_id>", methods=['GET', 'POST'])
def getUserImage(img_id):
    img_data = User_image().retrieve('*', f"img_id = {img_id}")
    if img_data:
        image = User_image(img_id=img_data[0][0], filename=None,
                           extension=img_data[0][2], img_data=img_data[0][3],
                           date_uploaded=img_data[0][4])
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route("/getRecipeImage/<int:img_id>", methods=['GET', 'POST'])
def getRecipeImage(img_id):
    img_data = Recipe_image().retrieve('*', f"img_id = {img_id}")
    if img_data:
        image = Recipe_image(img_id=img_data[0][0], filename=None,
                             extension=img_data[0][2], img_data=img_data[0][3],
                             date_uploaded=img_data[0][4])
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def createRecipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_image_id = 1
        if form.picture.data:
            recipe_image_id = createNewImage(form.picture.data, "Recipe")
        recipe = Recipe(title=form.title.data, content=form.content.data,
                        author_id=current_user.user_id, img_id=recipe_image_id)
        recipe.create()
        flash(f'Account updated!',
              'alert alert-success alert-dismissible fade show')
        return redirect(url_for('home'))
    return render_template('create_recipe.html', title='Create new recipe',
                           form=form)


@app.route("/recipe/<int:recipe_id>", methods=['GET'])
def recipe(recipe_id):
    recipeData = Recipe().retrieve("*", f"recipe_id = {recipe_id}")[0]
    if recipeData:
        recipe = Recipe(recipe_id=recipeData[0], title=recipeData[1], content=recipeData[2],
                        date_posted=recipeData[3], img_id=recipeData[4], author_id=recipeData[5])
    else:
        flash(f"Recipe you are looking for doesn't exist, sorry :(",
              'alert alert-danger alert-dismissible fade show')
        return redirect("home"), 404
    image_path = url_for('getRecipeImage', img_id=recipe.img_id)
    return render_template('recipe.html', title=recipe.title, image_path=image_path)

from os import path
import secrets
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from ucuzpisir import app, bcrypt
from ucuzpisir.forms import RegistrationForm, LoginForm, AccountUpdateForm, RecipeForm
from ucuzpisir.tables import User, UserImage, Recipe, RecipeImage, Ingredient, RecipeIngredient


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/home")
def home():
    recipes = Recipe().retrieve('*')
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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data,
                    password=hashed_password, email=form.email.data, birthdate=form.birthdate.data)
        user.create()  # Fix nad control
        flash(f'Account created for {form.username.data}!', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        users = User().retrieve('*', "email = %s", (form.email.data,))
        if users:
            user = users[0]
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
            flash(f'Login Unsuccessful. Please check e-mail and password', 'alert alert-danger alert-dismissible fade show')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    flash(f'Goodbye {current_user.username}!', 'alert alert-info alert-dismissible fade show')
    logout_user()
    return redirect(url_for('home'))


def create_new_image(form_picture_data, image_type):
    """
    param form_picture_data(image object): picture data from form
    param image_type(string): type of the image, ex: UserImage, RecipeImage
    returns: id of the created image
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = path.splitext(form_picture_data.filename)
    f_ext = f_ext[1:]
    if f_ext == 'jpg':
        f_ext = 'jpeg'
    if image_type == "User":
        image = UserImage(filename=random_hex, extension=f_ext, img_data=form_picture_data)
    elif image_type == "Recipe":
        image = RecipeImage(filename=random_hex, extension=f_ext, img_data=form_picture_data)
    image.create()
    images = image.retrieve('*', "filename = %s", (random_hex,))
    if images:
        image = images[0]
    else:
        image = None
        return 1
    return image.img_id


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.img_id != 1:
                UserImage().delete(img_id=current_user.img_id)
            current_user.img_id = create_new_image(form.picture.data, "User")
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.birthdate = form.birthdate.data
        current_user.update()
        flash(f'Account updated!', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.birthdate.data = current_user.birthdate
    image_path = url_for('get-user-image', img_id=current_user.img_id)
    return render_template('account.html', title='Account',
                           image_path=image_path, form=form)


@app.route("/get-user-image/<int:img_id>", methods=['GET', 'POST'])
def get_user_image(img_id):
    images = UserImage().retrieve('*', "img_id = %s", (img_id,))
    if images:
        image = images[0]
    else:
        return redirect(url_for('home')), 404
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route("/get-recipe-image/<int:img_id>", methods=['GET', 'POST'])
def get_recipe_image(img_id):
    images = RecipeImage().retrieve('*', "img_id = %s", (img_id,))
    if images:
        image = images[0]
    else:
        return redirect(url_for('home')), 404
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        if Recipe().retrieve('*', "title = %s", (form.title.data,)):
            flash(f'There is already a recipe like this!', 'alert alert-danger alert-dismissible fade show')
            return render_template('create_recipe.html', title='Create new recipe', form=form, legend='Tarif Oluştur')

        recipe_image_id = 1
        if form.picture.data:
            recipe_image_id = create_new_image(form.picture.data, "Recipe")
        recipe = Recipe(title=form.title.data, content=form.content.data,
                        author_id=current_user.user_id, img_id=recipe_image_id)
        recipe.create()
        recipe = Recipe().retrieve('*', "title = %s", (form.title.data,))[0]

        for ingredient in form.ingredients.data:
            if not Ingredient().retrieve('*', "name = %s", (ingredient['ingredient_name'],)):
                Ingredient(name=ingredient['ingredient_name'], calories=ingredient['calories'],
                           protein=ingredient['protein'], fat=ingredient['fat'],
                           carb=ingredient['carb']).create()
            ingredient_id = Ingredient().retrieve('*', "name = %s", (ingredient['ingredient_name'],))[0].ingredient_id
            RecipeIngredient(
                recipe_id=recipe.recipe_id,
                ingredient_id=ingredient_id,
                quantity=ingredient['quantity'],
                unit=ingredient['unit']
            ).create()

        flash(f'Recipe is created!', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('home'))
    return render_template('create_recipe.html', title='Create New Recipe',
                           form=form, legend='Tarif Oluştur')


@app.route("/recipe/<int:recipe_id>", methods=['GET'])
def recipe(recipe_id):
    recipes = Recipe().retrieve('*', "recipe_id = %s", (recipe_id,))
    ingredient_datas = RecipeIngredient().retrieve("ingredient_id, unit, quantity", "recipe_id = %s", (recipe_id,))
    ingredient_names = []
    for ingredient_data in ingredient_datas:
        ingredient_names.append(Ingredient().retrieve(
            "name", "ingredient_id = %s", (ingredient_data[0],))[0][0])

    if recipes:
        recipe = recipes[0]
    else:
        flash(f"Recipe you are looking for doesn't exist, sorry :(", 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('home')), 404

    image_path = url_for('get-recipe-image', img_id=recipe.img_id)
    author = User().retrieve('*', "user_id = %s", (recipe.author_id,))[0]
    return render_template('recipe.html', title=recipe.title, recipe=recipe,
                           image_path=image_path, author_username=author.username,
                           ingredient_names=ingredient_names, ingredient_datas=ingredient_datas)


@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipes = Recipe().retrieve('*', "recipe_id = %s", (recipe_id,))
    if recipes:
        recipe = recipes[0]
    else:
        flash(f"Recipe you are looking for doesn't exist, sorry :(", 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('home')), 404

    if recipe.author_id != current_user.user_id:
        flash(f"You are not supposed to be here, sorry. :(", 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('home')), 404

    form = RecipeForm()
    if request.method == 'GET':
        form.title.data = recipe.title
        form.content.data = recipe.content
    else:
        if form.picture.data:
            if recipe.img_id != 1:
                RecipeImage().delete(img_id=recipe.img_id)
            recipe.img_id = create_new_image(form.picture.data, "Recipe")

        recipe.title = form.title.data
        recipe.content = form.content.data
        recipe.update()
        flash('Your recipe has been updated!', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('recipe', recipe_id=recipe.recipe_id))

    return render_template('create_recipe.html', title='Update Recipe',
                           form=form, legend='Update Recipe')


@app.route("/recipe/<int:recipe_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_recipe(recipe_id):
    recipes = Recipe().retrieve('*', "recipe_id = %s", (recipe_id,))
    if recipes:
        recipe = recipes[0]
    else:
        flash(f"Recipe you are looking for doesn't exist, sorry :(", 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('home')), 404

    if recipe.author_id != current_user.user_id:
        flash(f"You are not supposed to be here, sorry. :(", 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('home')), 404

    recipe.delete()
    flash('Your recipe has been deleted!', 'alert alert-success alert-dismissible fade show')
    return redirect(url_for('home'))

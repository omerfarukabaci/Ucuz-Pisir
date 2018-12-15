from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ucuzpisir.tables import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    birthdate = DateField('Your birthdate')
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=80)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = User().retrieve('*', "username = %s", (username.data,))
        if users:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = User().retrieve('*', "email = %s", (email.data,))
        if users:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    birthdate = DateField('Your birthdate')
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=80)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            users = User().retrieve('*', "username = %s", (username.data,))
            if users:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            users = User().retrieve('*', "email = %s", (email.data,))
            if users:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class RecipeForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=8, max=50)])
    content = TextAreaField('Recipe instructions',
                            validators=[DataRequired(), Length(min=80)])
    submit = SubmitField('Submit')

    picture = FileField('Update Meal Image', validators=[
                    FileAllowed(['jpg', 'jpeg', 'png'])])

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    birthdate = DateTimeField('Your birthdate', format='%d/%m/%Y',
                              render_kw={"placeholder": "DD/MM/YYYY"})
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=80)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

#    def validate_username(self, username):

#        following check is on sqlalchemy, fix this
#        user = User.query.filter_by(username=username.data).first()
#        if user:
#            raise ValidationError('That username is taken. Please choose a different one.')


#    def validate_email(self, email):

#        following check is on sqlalchemy, fix this
#        user = User.query.filter_by(email=email.data).first()
#        if user:
#            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

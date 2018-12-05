from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from ucuzpisir import routes #Reminder: There is a reason this line is here but not on top.
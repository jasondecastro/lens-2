from flask import Flask

 
app = Flask(__name__)

import random
app.jinja_env.globals.update(randint=random.randint)
 
app.secret_key = 'development key'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/lens'
 
from models import db
db.init_app(app)

import src.routes

from flask.ext.mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)



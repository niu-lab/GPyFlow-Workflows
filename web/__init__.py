from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
whooshee = Whooshee()
whooshee.init_app(app)

from web import views
from web import models

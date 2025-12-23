import os
from flask import Flask, render_template, Blueprint
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
from .models.shared import db
from .blueprints import login

app = Flask(__name__)

config = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": 3306,
    "database": os.getenv("DB_DATABASE"),
}

url = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}".format(
    config["user"],
    config["password"],
    config["host"],
    config["port"],
    config["database"],
)
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

# db = SQLAlchemy(app)
db.init_app(app)
app.register_blueprint(login.bp)

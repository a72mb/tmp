import os
from dotenv import load_dotenv
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from .models.shared import db
from .models.users import User
from .blueprints import login,main

load_dotenv()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')

db.init_app(app)
app.register_blueprint(login.bp)
app.register_blueprint(main.bp)

login_manager = LoginManager(app)
login_manager.login_view = 'login.login' #type:ignore
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

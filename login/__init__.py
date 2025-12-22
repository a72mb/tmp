import os
from dotenv import load_dotenv
from typing import List, Dict
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from login import login,pages,errors,database
import pathlib

load_dotenv()

basedir = pathlib.Path(__file__).parent.resolve()

# def create_app():
app =Flask(__name__)
app.config.from_prefixed_env()
app.logger.setLevel("INFO")
app.secret_key = app.config.get('SECRET_KEY')

# database.init_app(app)

app.register_blueprint(login.bp)
# app.register_blueprint(pages.bp)
app.register_error_handler(404, errors.page_not_found)
# app.logger.info(f"Current Environment: {os.getenv('ENVIRONMENT')}")
# app.logger.info(f"Using Database: {app.config.get('DATABASE')}")
    # return app
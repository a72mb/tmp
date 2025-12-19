import os
from dotenv import load_dotenv
from typing import List, Dict
from flask import Flask

from login import login,errors,database
import pathlib

load_dotenv()

basedir = pathlib.Path(__file__).parent.resolve()

# def create_app():
app =Flask(__name__)
app.config.from_prefixed_env()
app.logger.setLevel("INFO")
app.secret_key = app.config.get('SECRET_KEY')

database.init_app(app)

app.register_blueprint(login.bp)
app.register_error_handler(404, errors.page_not_found)
# app.logger.info(f"Current Environment: {os.getenv('ENVIRONMENT')}")
# app.logger.info(f"Using Database: {app.config.get('DATABASE')}")
    # return app
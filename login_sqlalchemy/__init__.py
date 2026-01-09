import os
from dotenv import load_dotenv
from flask import Flask,send_from_directory
from flask_login import LoginManager
from flask_restful import Api
from .models.shared import db
from .models.users import User
from .blueprints import login,main
from .resources.user_resource import UserResource

load_dotenv()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
api = Api(app)
api.add_resource(UserResource, '/users/<int:user_id>', '/users')
db.init_app(app)
app.register_blueprint(login.bp)
app.register_blueprint(main.bp)

login_manager = LoginManager(app)
login_manager.login_view = 'login.login' #type:ignore
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Was going to use this for serving npm packages but decided against it for now
@app.route('/npm/<path:package>/<path:filename>') # type: ignore
def serve_npm_package(package, filename):
    npm_path = os.path.join('node_modules', package)
    return send_from_directory("../"+npm_path, filename)
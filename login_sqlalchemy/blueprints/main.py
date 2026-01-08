from flask import Blueprint, flash, render_template,request,url_for,session,redirect
from flask_login import login_user, login_required,current_user
from login_sqlalchemy.models import shared
db = shared.db
from login_sqlalchemy.models.users import User

bp = Blueprint("main", __name__)

@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html',current_user=current_user)
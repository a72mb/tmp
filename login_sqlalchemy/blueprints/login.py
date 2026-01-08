from flask import Blueprint, flash, render_template,request,url_for,session,redirect
from flask_login import login_user,logout_user
from login_sqlalchemy.models import shared
db = shared.db
from login_sqlalchemy.forms.registration_form import RegistrationForm
from login_sqlalchemy.forms.login_form import LoginForm
from login_sqlalchemy.models.users import User
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("login", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):  # type: ignore # Compare hashed passwords
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)  # type: ignore # Hash password here
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)#type:ignore
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login.login'))    
    return render_template("sign_up.html", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login.login'))
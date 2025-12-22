from doctest import debug
from flask import Blueprint, render_template,request,url_for,session,redirect
from sqlalchemy import text
from sqlalchemy.orm import Session
from login.database import get_db

bp = Blueprint("login", __name__)

@bp.route("/")
@bp.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = get_db()
        if connection is None:
            msg = 'Database connection error!'
            return redirect(url_for('login.login', msg=msg))

        stmt=text('SELECT * FROM accounts WHERE username = :usr AND password = :pwd limit 1')
        with Session(connection) as session:
            result = session.execute(stmt, {'usr': username, 'pwd': password})
            account = result.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id'] #type:ignore
            session['username'] = account['username'] #type:ignore
            return render_template("app/index.html", msg=msg)
            # return redirect(url_for('app.index', msg='Logged in successfully!'))
        else:
            msg = 'Incorrect username/password!'
    return render_template("login/form.html", msg=msg)

@bp.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login.login'))

@bp.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        connection = get_db()
        if connection is None:
            msg = 'Database connection error!'
            return redirect(url_for('login.register', msg=msg))
        stmt=text('SELECT * FROM accounts WHERE username = :usr')
        result=connection.execute(stmt, {'usr': username})
        account = result.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            stmt=text('INSERT INTO accounts (username, password, email) VALUES (:usr, :pwd, :email)')
            connection.execute(stmt, {'usr': username, 'pwd': password, 'email': email})
            connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login/form.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("login/register.html", msg=msg)
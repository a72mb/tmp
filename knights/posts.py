from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from knights.database import get_db

bp = Blueprint("posts", __name__)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        author = request.form["author"] or "Anonymous"
        message = request.form["message"]

        if message:
            db = get_db()
            if db:
                cursor = db.cursor(dictionary=True)
                cursor.execute(
                    "INSERT INTO post (author, message) VALUES (%s, %s)",
                    (author, message),
                )
                db.commit()
                current_app.logger.info(f"New post by {author}")
                flash(f"Thanks for posting, {author}!", category="success")
                return redirect(url_for("posts.posts"))
            else:
                current_app.logger.exception(f"Could not connect to database.")
                flash("Could not connect to database.", category="error")
        else:
            flash("You need to post a message.", category="error")
    return render_template("posts/create.html")


@bp.route("/posts")
def posts():
    db = get_db()
    if db:
        cursor=db.cursor(dictionary=True)
        cursor.execute(
            "SELECT author, message, created FROM post ORDER BY created DESC"
        )
        posts=cursor.fetchall()
    else:
        posts={}
    return render_template("posts/posts.html", posts=posts)

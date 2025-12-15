# app.py

from flask import Flask,render_template #type:ignore
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()
app =Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
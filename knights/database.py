import mysql.connector
import os
import click
from flask import current_app, g


def init_app(app):
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command():
    db = get_db()
    if(db != None):
        cursor=db.cursor()
        with current_app.open_resource("schema.sql") as f:
            cursor.execute(f.read().decode("utf-8"))
            # click.echo(f.read().decode("utf-8"))
        click.echo("You successfully initialized the database!")
    else:
        click.echo("Failed to connect to the database.")

def get_db():
    connection=None
    config = {
        'user': os.getenv("DB_USERNAME"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'port': 3306,
        'database': os.getenv("DB_DATABASE")
    }
    try:
        connection = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        if connection!=None:
            connection.close()
        connection=None
    return connection
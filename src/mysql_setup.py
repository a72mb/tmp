from dotenv import load_dotenv #type:ignore

load_dotenv()
import os
import MySQLdb
import datetime

try:
    connection = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_DATABASE"),
    )

    cur = connection.cursor()
    cur.execute(""" select * from entity """)
    for row in cur:
        pass
        # print(row)
        # print("<br>")
except Exception as e:
    print(e)
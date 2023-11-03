from flask import Flask, app, render_template
import psycopg2
import util

app = Flask(__name__)

conn = psycopg2.connect(
    database = "dvdrental",
    user = 'raywu1990',
    password = 'test',
    host = '127.0.0.1',
    port = '5432'
)

database = 'dvdrental'
username = 'raywu1990'
password = 'test'
host = '127.0.0.1'
port = '5432'

def connect_to_db():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.Error as e:
        return None, None

def disconnect_from_db(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

@app.route("/api/update_basket_a")
def insert_cherry():
    conn, cursor = connect_to_db()

    if not conn:
        return "<p>Database Connection Error</p>"

    try:
        sql_query = "INSERT INTO basket_a VALUES (5, 'Cherry');"
        cursor.execute(sql_query)
        conn.commit()
        return "<p>Success</p>"
    except psycopg2.Error as e:
        return f"<p>Error: {e}</p>"
    finally:
        disconnect_from_db(conn, cursor)

@app.route("/api/unique")
def unique_fruits():
    conn, cursor = connect_to_db()

    if not conn:
        return "<p>Database Connection Error</p>"

    try:
        sql_query = """
            SELECT DISTINCT fruit_a, 'basket_a' as source FROM basket_a
            UNION
            SELECT DISTINCT fruit_b, 'basket_b' as source FROM basket_b
        """
        cursor.execute(sql_query)
        unique_fruits = cursor.fetchall()
        
        grouped_fruits = {}
        for fruit, source in unique_fruits:
            if fruit not in grouped_fruits:
                grouped_fruits[fruit] = source
    except psycopg2.Error as e:
        return f"<p>SQL ERROR: {e}</p>"
    finally:
        disconnect_from_db(conn, cursor)

    return render_template("uniquefruittable.html", grouped_fruits=grouped_fruits)

if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1")

from flask import Flask, render_template
import mysql.connector
from contextlib import contextmanager
from routing_copy import main

# MySQL connection details
host = "localhost"
user = "root"
password = "dataset2024"
database = "customer_service"

app = Flask(__name__)

# Database connection manager
@contextmanager
def get_db_connection():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    try:
        yield connection
    finally:
        connection.close()

# Retrieve all unique user_ids from interactions table
def get_unique_customer_keys():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT DISTINCT user_id FROM interactions"
        cursor.execute(query)
        
        # Fetch all unique user_ids
        return [customer_key[0] for customer_key in cursor.fetchall()]

# Retrieve user summary from customer_summary table
def retrieve_user_summary(user_id):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT user_id, summary FROM customer_summary WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            return {"user_id": result[0], "summary": result[1]}
        else:
            return {"user_id": user_id, "summary": "No summary available."}  # Return a placeholder if no summary

# Flask route for customer service agent dashboard
@app.route("/")
def customer_summary():
    # Get all unique user_ids
    user_ids = get_unique_customer_keys()

    # Retrieve summaries for each user_id
    user_summaries = []
    no_summary_users = []  # List to track users without summaries
    for user_id in user_ids:
        user_summary = retrieve_user_summary(user_id)
        if user_summary:
            user_summaries.append(user_summary)
        else:
            no_summary_users.append(user_id)

    # Pass both user_summaries and no_summary_users to the template
    return render_template("agent/index.html", user_summaries=user_summaries, no_summary_users=no_summary_users)

if __name__ == "__main__":
   main()
   app.run(debug=True, host='127.0.0.1', port=5003)
